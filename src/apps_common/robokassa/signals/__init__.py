from django.dispatch import Signal

robokassa_paid = Signal(providing_args=['inv_id', 'out_sum', 'extra'])
