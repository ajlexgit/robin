class Icon:
    def __init__(self, url='', name='', position=()):
        self.url = url
        self._name = name
        self._position = position

    def __getitem__(self, item):
        return self._position[item]

    def __bool__(self):
        return bool(self._name and self._position)

    def __str__(self):
        return self._name
