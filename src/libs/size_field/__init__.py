from .models import SizeField

"""
    Поле для ввода размера чего-либо в виде двух цифр.
    
    Пример:
        size = SizeField('размер', min_value='50x50', max_value=(100, 150), default='100x100')
"""