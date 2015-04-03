class Size:
    """ Класс размера """
    def __init__(self, width=0, height=0):
        self._width = int(width)
        self._height = int(height)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __bool__(self):
        return bool(self._width or self._height)

    def __str__(self):
        return '{}x{}'.format(self._width, self._height)
        