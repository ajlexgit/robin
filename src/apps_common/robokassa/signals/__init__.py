from django.dispatch import Signal

robokassa_result = Signal(providing_args=['data'])
robokassa_success = Signal(providing_args=['data'])
robokassa_fail = Signal(providing_args=['data'])

