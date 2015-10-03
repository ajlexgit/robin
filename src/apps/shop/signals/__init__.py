from django.dispatch import Signal

products_changed = Signal(providing_args=['categories'])
categories_changed = Signal(providing_args=['categories', 'include_self'])
order_payed = Signal(providing_args=['order'])