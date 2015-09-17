from django.dispatch import Signal

order_payed = Signal(providing_args=['order'])