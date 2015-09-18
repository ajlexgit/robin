import re

re_price = re.compile(r'^(-?\d+)(\d{3})')


def split_price(value, join=' '):
    """ Разделение цены по разрядам """
    new = re_price.sub('\\1{}\\2'.format(join), value)
    if value == new:
        return new
    else:
        return split_price(new, join)
