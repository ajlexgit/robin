import logging
from time import sleep
from itertools import islice, chain
from django.db import models
from django.utils.timezone import now
from django.db.utils import IntegrityError
from django.core.management import BaseCommand
from ...models import MailerConfig, Group, Campaign, Subscriber
from ... import conf
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
                sleep(0.1)

    def export_groups(self):
        """ Отправка групп в MailerLite """
        logger.info("Export groups...")
        for group in Group.objects.all():
            try:
                if group.status == Group.STATUS_QUEUED:
                    response = api.groups.create(
                        name=group.name,
                    )
                    group.status = Group.STATUS_PUBLISHED
                else:
                    response = api.groups.update(
                        group.remote_id,
                        name=group.name,
                    )
            except api.SubscribeAPIError as e:
                logger.error(e.message)
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
                    status=Group.STATUS_PUBLISHED,
                )
                logger.info("Group '%s' created." % remote_group['name'])

            # обновляем поля локальной группы
            local_group.update_from(remote_group)
            local_group.save()

    def export_campaigns(self):
        """ Отправка рассылок в MailerLite """
        logger.info("Export campaigns...")
        campaigns = Campaign.objects.filter(status=Campaign.STATUS_QUEUED)
        for campaign in campaigns:
            if not campaign.published:
                # Publish campaign
                if not campaign.remote_id:
                    try:
                        response = api.campaings.create(
                            subject=campaign.subject,
                            groups=[group.remote_id for group in campaign.groups.all()],
                            from_email=self.config.from_email,
                            from_name=self.config.from_name,
                        )
                    except api.SubscribeAPIError as e:
                        logger.error(e.message)
                        continue
                    else:
                        campaign.remote_id = response['id']
                        campaign.remote_mail_id = response['mail_id']
                        campaign.save()
                        logger.info("Published campaign '%s'" % campaign.subject)

                # Set content
                try:
                    api.campaings.content(
                        campaign.remote_id,
                        html=campaign.render_html(scheme='https://' if conf.HTTPS_ALLOWED else 'http://'),
                        plain=campaign.render_plain(),
                    )
                except api.SubscribeAPIError as e:
                    logger.error(e.message)
                    continue
                else:
                    campaign.published = True
                    campaign.save()
                    logger.info("Setted content for campaign '%s'" % campaign.subject)

            # Start
            elif campaign.remote_id:
                try:
                    api.campaings.run(campaign.remote_id)
                except api.SubscribeAPIError as e:
                    logger.error(e.message)
                else:
                    campaign.status = Campaign.STATUS_RUNNING
                    campaign.save()
                    logger.info("Started campaign '%s'" % campaign.subject)
            else:
                logger.warning("Campaign #%s doesn\'t have remote ID" % campaign.pk)

    def import_campaigns(self, status='sent'):
        """ Загрузка рассылок """
        logger.info("Import campaigns with status '%s'..." % status)
        for remote_campaign in self.all_pages(api.campaings.get_all, status):
            local_campaign, created = Campaign.objects.get_or_create(
                remote_id=remote_campaign['id']
            )
            if created:
                logger.info("Campaign '%s' created." % remote_campaign['name'])

            # Если рассылка запланирована, но ещё не начата, то импорт сбросит статус
            if local_campaign.status != Campaign.STATUS_QUEUED:
                local_campaign.update_from(remote_campaign)
                local_campaign.save()

    def import_subscribers(self):
        """ Загрузка подписчиков """
        logger.info("Import subscribers...")
        for group in Group.objects.all():
            for remote_subscriber in self.all_pages(api.groups.subscribers, group.remote_id):
                try:
                    local_subscriber = Subscriber.objects.get(
                        models.Q(remote_id=remote_subscriber['id']) |
                        models.Q(email=remote_subscriber['email'], remote_id=0)
                    )
                except Subscriber.MultipleObjectsReturned:
                    logger.info("MultipleObjectsReturned for ({0[id]}, {0[email]}).".format(remote_subscriber))
                    continue
                except Subscriber.DoesNotExist:
                    local_subscriber = Subscriber()
                    logger.info("Subscriber '{0[email]}' created.".format(remote_subscriber))

                local_subscriber.update_from(remote_subscriber)
                try:
                    local_subscriber.save()
                except IntegrityError:
                    logger.warning("IntegrityError for ({0[id]}, {0[email]})".format(remote_subscriber))
                    continue

                if not local_subscriber.groups.filter(pk=group.pk).exists():
                    local_subscriber.groups.add(group)

    def export_subscribers(self, group):
        """ Отправка новых подписчиков в MailerLite """
        logger.info("Export subscribers...")
        subscribers = Subscriber.objects.filter(
            groups=group,
            status=Subscriber.STATUS_QUEUED,
        ).distinct()
        subscribers_iter = subscribers.iterator()

        while True:
            data = tuple(
                api.subscribers.prepare_subscriber(
                    subscriber.email,
                    first_name=subscriber.name,
                    last_name=subscriber.last_name,
                    company=subscriber.company,
                )
                for subscriber in islice(subscribers_iter, 100)
            )
            if not data:
                break

            try:
                response = api.subscribers.bulk_create(group.remote_id, data, resubscribe=True)
            except api.SubscribeAPIError as e:
                logger.error(e.message)
            else:
                for row in chain(response['imported'], response['updated'], response['unchanged']):
                    subscribers.filter(email=row['email']).update(
                        remote_id=row['id'],
                        status=Subscriber.STATUS_SUBSCRIBED,
                    )
                    logger.info("Exported subscriber '{0[email]}'".format(row))

                for row in response['errors']:
                    logger.error('%r' % row)

    def handle(self, *args, **options):
        self.config = MailerConfig.get_solo()

        # Groups
        if options['export_groups']:
            self.export_groups()
            self.config.export_groups_date = now()

        if options['import_groups']:
            self.import_groups()
            self.config.import_groups_date = now()

        # Subscribers
        if options['export_subscribers']:
            for group in Group.objects.all():
                self.export_subscribers(group)
            self.config.export_subscribers_date = now()

        if options['import_subscribers']:
            try:
                self.import_subscribers()
            except api.SubscribeAPIError as e:
                logger.error(e.message)
            else:
                self.config.import_subscribers_date = now()

        # Campaigns
        if options['export_campaigns']:
            self.export_campaigns()
            self.config.export_campaigns_date = now()

        if options['import_campaigns']:
            for status in ['draft', 'outbox', 'sent']:
                self.import_campaigns(status)
            self.config.import_campaigns_date = now()

        self.config.save()
