from django.dispatch import Signal

products_changed = Signal(providing_args=['categories'])
categories_changed = Signal(providing_args=['categories', 'include_self'])
order_cancelled = Signal(providing_args=['order'])
order_paid = Signal(providing_args=['order'])
