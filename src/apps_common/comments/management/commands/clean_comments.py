from django.core.management.base import NoArgsCommand
from ...models import Comment


class Command(NoArgsCommand):
    """
        Физическое удаление комментариев, которые отмечены как удаленные и невидимы
    """
    help = 'Removes comments which marked as deleted'

    def handle_noargs(self, **options):
        check_valid = Comment.objects.filter(deleted=False, visible=False)
        if check_valid.exists():
            self.stdout.write('ERROR: there are hidden comments which are not deleted!')
            self.stdout.write(check_valid)
            return

        deleted = Comment.objects.filter(deleted=True, visible=False)
        count = deleted.count()
        deleted.delete()

        self.stdout.write('Deleted {} comments'.format(count))
