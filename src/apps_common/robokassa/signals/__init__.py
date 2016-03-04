from django.dispatch import Signal

robokassa_success = Signal(providing_args=['inv_id', 'request', 'extra'])
