# -*- coding: utf-8 -*-

from django.dispatch import Signal

payment_process = Signal(providing_args=['instance', 'site'])
payment_completed = Signal(providing_args=['instance', 'site'])