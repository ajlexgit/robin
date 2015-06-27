class Coords:
    _lat = None
    _lng = None

    def __init__(self, lng=None, lat=None):
        self.lng = lng
        self.lat = lat

    @property
    def lng(self):
        return self._lng

    @lng.setter
    def lng(self, value):
        try:
            self._lng = float(value)
        except (ValueError, TypeError):
            self._lng = None

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        try:
            self._lat = float(value)
        except (ValueError, TypeError):
            self._lat = None

    def __bool__(self):
        return self.lng is not None and self.lat is not None

    def __iter__(self):
        if self:
            return iter((self._lng, self._lat))

    def __repr__(self):
        if self:
            return '{0}, {1}'.format(self.lng, self.lat)
        else:
            return ''
