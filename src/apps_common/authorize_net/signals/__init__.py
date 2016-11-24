from django.dispatch import Signal

authorizenet_success = Signal(providing_args=['invoice', 'request'])
authorizenet_error = Signal(providing_args=['invoice', 'request', 'code', 'reason'])
