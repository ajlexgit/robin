from django.dispatch import Signal

paypal_success = Signal(providing_args=['invoice', 'request', 'items'])
paypal_error = Signal(providing_args=['invoice', 'request', 'items'])
