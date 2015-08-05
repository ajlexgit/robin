import re

re_hexcolor = re.compile('^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$')


def color_from_string(value):
    """
        Превращение строки цвета в формате "#Fcc" / "Fcc" / "#FFcc00" / "FFcc00"
        в шестизначный формат без ведущей решетки ("FFCC00")
    """
    color_match = re_hexcolor.match(str(value))
    if not color_match:
        return None

    no_hash_color = color_match.group(1)
    if len(no_hash_color) == 3:
        return ''.join(letter * 2 for letter in no_hash_color).upper()
    else:
        return no_hash_color.upper()
