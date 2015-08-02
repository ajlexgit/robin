# Провайдеры видео
PROVIDER_YOUTUBE = 1
def youtube_preview(video_key):
    return 'http://img.youtube.com/vi/%s/mqdefault.jpg' % video_key

PROVIDER_VIMEO = 2
def vimeo_preview(video_key):
    from urllib import request, error
    from xml.dom import minidom

    try:
        result = request.urlopen('http://vimeo.com/api/v2/video/%s.xml' % video_key, timeout=2)
    except error.URLError as e:
        raise ConnectionError('Ошибка Vimeo: %s' % e.reason)

    if result.status == 200:
        dom = minidom.parseString(result.read())
        element = dom.getElementsByTagName('thumbnail_large').item(0)
        if element is None:
            raise ConnectionError('Ошибка Vimeo: превью не найдено')

        link = element.firstChild.data
        link = link.replace('640.', '320.')
        link = link.replace('webp', 'jpg')
        return link
    raise ConnectionError('Ошибка Vimeo: ответ сервера %s' % result.status)

PROVIDERS = {
    PROVIDER_YOUTUBE: {
        'browse_url': '//www.youtube.com/watch?v={video_key}',
        'preview_url': youtube_preview,
        'link_patterns': (
            r'https?://www.youtube.com/watch\?v=([-\w]+)',
            r'https?://www.youtube.com/v/([-\w]+)',
            r'https?://youtu.be/([-\w]+)'
        )
    },
    PROVIDER_VIMEO: {
        'browse_url': '//vimeo.com/{video_key}',
        'preview_url': vimeo_preview,
        'link_patterns': (
            r'https?://vimeo.com/channels/[^/]+/(\d+)',
            r'https?://vimeo.com/(\d+)',
        )
    }
}
