from django.dispatch import Signal

visible_products_changed = Signal(providing_args=['categories'])
order_payed = Signal(providing_args=['order'])