from django.dispatch import receiver
from . import robokassa_result, robokassa_success, robokassa_fail


@receiver(robokassa_result)
def result_received_handler(sender, **kwargs):
    data = kwargs['data']


@receiver(robokassa_success)
def success_page_visited_handler(sender, **kwargs):
    data = kwargs['data']


@receiver(robokassa_fail)
def fail_page_visited_handler(sender, **kwargs):
    data = kwargs['data']

