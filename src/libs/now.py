from django.utils import timezone


def now():
    """ Текущее время с учетом текущей временной зоны """
    return timezone.localtime(timezone.now())