from django.dispatch import receiver
from . import robokassa_paid


@receiver(robokassa_paid)
def robokassa_paid_handler(sender, **kwargs):
    inv_id = kwargs['inv_id']
    out_sum = kwargs['out_sum']
    extra = kwargs['extra']
