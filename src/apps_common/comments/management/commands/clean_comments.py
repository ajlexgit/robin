from django.core.management import BaseCommand
from ...models import Comment


class Command(BaseCommand):
    """ Физическое удаление комментариев, которые отмечены как удаленные и невидимы """
    def handle(self, *args, **options):
        check_valid = Comment.objects.filter(deleted=False, visible=False)
        if check_valid.exists():
            print('ERROR: there are hidden comments which are not deleted!')
            print(check_valid)
            return
        
        deleted = Comment.objects.filter(deleted=True, visible=False)
        count = deleted.count()
        deleted.delete()
        
        print('Deleted {} comments'.format(count))