from django.dispatch import Signal

gotobilling_success = Signal(providing_args=['inv_id', 'request'])
gotobilling_error = Signal(providing_args=['inv_id', 'request', 'code', 'reason'])
