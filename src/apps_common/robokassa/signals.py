from django.dispatch import Signal

result_received = Signal(providing_args=['inv_id', 'out_sum', 'extra', 'site'])

