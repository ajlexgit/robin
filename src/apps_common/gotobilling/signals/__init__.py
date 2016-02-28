from django.dispatch import Signal

gotobilling_paid = Signal(providing_args=['inv_id', 'amount'])
gotobilling_error = Signal(providing_args=['inv_id', 'code', 'reason'])
