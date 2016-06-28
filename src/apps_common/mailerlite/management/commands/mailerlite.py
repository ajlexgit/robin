import logging
from time import sleep
from django.utils.timezone import now
from django.core.management import BaseCommand
from ...models import MailerConfig, Group, Campaign, Subscriber
from ... import api

logger = logging.getLogger('mailerlite')


class Command(BaseCommand):
    """
        Синхронизация данных
    """
    config = None

    def add_arguments(self, parser):
        parser.add_argument('-eg', '--export-groups',
            action='store_true',
            dest='export_groups',
            help='Export groups'
        )
        parser.add_argument('-ig', '--import-groups',
            action='store_true',
            dest='import_groups',
            help='Import groups'
        )

        parser.add_argument('-ec', '--export-campaigns',
            action='store_true',
            dest='export_campaigns',
            help='Export campaigns'
        )
        parser.add_argument('-ic', '--import-campaigns',
            action='store_true',
            dest='import_campaigns',
            help='Import campaigns'
        )

        parser.add_argument('-is', '--import-subscribers',
            action='store_true',
            dest='import_subscribers',
            help='Import subscribers'
        )
        parser.add_argument('-es', '--export-subscribers',
            action='store_true',
            dest='export_subscribers',
            help='Export subscribers'
        )

    def all_pages(self, import_func, *args, limit=100, **kwargs):
        page = 0
        kwargs['limit'] = limit
        while True:
            kwargs['offset'] = page * limit

            try:
                items = import_func(*args, **kwargs)
            except api.SubscribeAPIError as e:
                logger.error(e.message)
                return

            for item in items:
                yield item

            if len(items) < limit:
                break
            else:
                page += 1
                sleep(0.2)

    def all_pages_v1(self, import_func, *args, limit=1000, **kwargs):
        page = 0
        while True:
            try:
                items = import_func(*args, limit=limit, page=page, **kwargs)
            except api.SubscribeAPIError as e:
                logger.error(e.message)
                return

            for item in items:
                yield item

            if len(items) < limit:
                break
            else:
                page += 1
                sleep(0.2)

    def export_groups(self):
        """ Отправка групп в MailerLite """
        logger.info("Export groups...")
        for group in Group.objects.all():
            try:
                if group.remote_id:
                    response = api.groups.update(
                        group.remote_id,
                        name=group.name,
                    )
                else:
                    response = api.groups.create(
                        name=group.name,
                    )
            except api.SubscribeAPIError as e:
                logging.error(e.message)
            else:
                group.remote_id = response['id']
                group.save()

    def import_groups(self):
        """ Загрузка групп """
        logger.info('Import groups...')
        for remote_group in self.all_pages(api.groups.get_all):
            try:
                local_group = Group.objects.get(remote_id=remote_group['id'])
            except Group.DoesNotExist:
                # создание локальной группы если её нет
                local_group = Group(
                    name=remote_group['name'],
                )
                logger.info("Group '%s' created." % remote_group['name'])

            # обновляем поля локальной группы
            local_group.update_from(remote_group)
            local_group.save()

    def export_campaigns(self):
        """ Отправка рассылок в MailerLite """
        logger.info("Export campaigns...")
        for campaign in Campaign.objects.filter(status=Campaign.STATUS_QUEUED):
            if not campaign.remote_id:
                try:
                    response = api.campaings.create(
                        subject=campaign.subject,
                        groups=[group.remote_id for group in campaign.groups.all()],
                        from_email=self.config.from_email,
                        from_name=self.config.from_name,
                    )
                except api.SubscribeAPIError as e:
                    logging.error(e.message)
                else:
                    campaign.remote_id = response['id']
                    campaign.remote_mail_id = response['mail_id']
                    campaign.save()

            # Set content
            try:
                api.campaings.content(
                    campaign.remote_id,
                    html=campaign.render_html(scheme='http://'),
                    plain=campaign.render_plain(),
                )
            except api.SubscribeAPIError as e:
                logging.error(e.message)

    def import_campaigns(self):
        """ Загрузка рассылок """
        logger.info('Import campaigns...')
        for remote_campaign in self.all_pages_v1(api.campaings.get_all):
            try:
                local_campaign = Campaign.objects.get(remote_mail_id=remote_campaign['id'])
            except Campaign.DoesNotExist:
                # создание локальной рассылки если её нет
                local_campaign = Campaign()
                logger.info("Campaign '%s' created." % remote_campaign['subject'])

            # обновляем поля локальной группы
            local_campaign.update_from(remote_campaign, version=1)
            local_campaign.save()

    def import_subscribers(self):
        """ Загрузка подписчиков """
        logger.info("Import subscribers...")
        for group in Group.objects.all():
            for remote_subscriber in self.all_pages(api.groups.subscribers, group.remote_id):
                try:
                    local_subscriber = Subscriber.objects.get(remote_id=remote_subscriber['id'])
                except Subscriber.DoesNotExist:
                    local_subscriber = Subscriber()
                    logger.info("Subscriber '%s' created." % remote_subscriber['email'])

                local_subscriber.update_from(remote_subscriber)
                local_subscriber.save()

                if not local_subscriber.groups.filter(pk=group.pk).exists():
                    local_subscriber.groups.add(group)

    def export_subscribers(self, group):
        """ Отправка новых подписчиков в MailerLite """
        logger.info("Export subscribers...")
        new_subscribers = Subscriber.objects.filter(
            groups=group,
            date_created__gte=self.config.export_subscribers_date
        ).distinct()
        for subscriber in new_subscribers:
            try:
                response = api.subscribers.create(
                    group.remote_id,
                    email=subscriber.email,
                    first_name=subscriber.name,
                    last_name=subscriber.last_name,
                    company=subscriber.company,
                    status='subscribed',
                )
            except api.SubscribeAPIError as e:
                logging.error(e.message)
            else:
                subscriber.remote_id = response['id']
                subscriber.save()

    def handle(self, *args, **options):
        self.config = MailerConfig.get_solo()

        # Groups
        if options['export_groups']:
            self.export_groups()
            self.config.export_groups_date = now()

        if options['import_groups']:
            self.import_groups()
            self.config.import_groups_date = now()

        # Campaigns
        if options['export_campaigns']:
            self.export_campaigns()
            self.config.export_campaigns_date = now()

        if options['import_campaigns']:
            self.import_campaigns()
            self.config.import_campaigns_date = now()

        # Subscribers
        if options['export_subscribers']:
            for group_id in Group.objects.values_list('remote_id'):
                self.export_subscribers(group_id)
            self.config.export_subscribers_date = now()

        if options['import_subscribers']:
            try:
                self.import_subscribers()
            except api.SubscribeAPIError as e:
                logging.error(e.message)
            else:
                self.config.import_subscribers_date = now()

        self.config.save()
