import re
from .providers import PROVIDERS

re_url = re.compile(r'(?:https?:)?//')


class VideoLink:
    __slots__ = ('_provider', '_key', '_info', '_url')

    def __new__(cls, link):
        self = object.__new__(cls)

        if re_url.match(link):
            # url
            for provider in PROVIDERS.values():
                try:
                    self._provider, self._key = provider.parse(link)
                    break
                except ValueError:
                    pass
            else:
                raise ValueError('Invalid video URL: %s' % link)
        else:
            # video_key
            self._provider, self._key = link.split('#', 1)

        self._url = None
        self._info = None
        return self

    @property
    def provider(self):
        return PROVIDERS.get(self._provider)

    @property
    def key(self):
        return self._key

    @property
    def url(self):
        if self._url is None:
            self._url = self.provider.build_url(self._key)
        return self._url

    @property
    def info(self):
        if self._info is None:
            self._info = self.provider.get_info(self._key)
        return self._info

    @property
    def db_value(self):
        return '{}#{}'.format(self._provider, self._key)

    def __repr__(self):
        return self.url