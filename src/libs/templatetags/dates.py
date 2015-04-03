import re
from django.conf import settings
from django.template import Library, defaultfilters
from django.utils import timezone
from django.utils.translation import ugettext as _

register = Library()

year_re = re.compile('[\s\.]+(Y|y)')


@register.filter(expects_localtime=True)
def shortdate(value):
    """
        Выводит дату и время с учетом разницы во времени:
        
        сегодня, 21:00
        вчера, 21:00
        16 февраля, 21:00       # текущий год
        16 февраля 2014, 21:00  # другой год
    """
    now = timezone.localtime(timezone.now())
    diff = now - value
    
    if diff < timezone.timedelta():
        return defaultfilters.date(value)
    elif diff < timezone.timedelta(1):
        return '%s, %s' % (_('today'), defaultfilters.time(value))
    elif diff < timezone.timedelta(2):
        return '%s, %s' % (_('yesterday'), defaultfilters.time(value))
    else:
        date_format = None
        if now.year == value.year:
            date_format = year_re.sub('', settings.DATE_FORMAT)
        date = defaultfilters.date(value, date_format)
        time = defaultfilters.time(value)
        return '%s, %s' % (date, time)
