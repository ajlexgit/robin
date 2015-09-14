import requests

# Документация
# https://developers.google.com/youtube/v3/getting-started

API_URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = 'AIzaSyDUyHc1otYjl7Hprm-mL5UxwygSivJNfaE'
CHANNEL_ID = 'UChQJPNUnC1zeWqk6v4lPWsg'
PLAYLIST_ID = 'PLTOwwDVdFdOxqCcJkYJMf-KpzA70ERjIB'


def _get(resource, data):
    default = {
        'key': API_KEY,
    }
    default.update(data)

    response = requests.get('%s%s' % (API_URL, resource), params=default)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError('API response: %s' % response.status_code)


def get_channel_playlists(channel_id=CHANNEL_ID):
    """ Список плейлистов канала """
    result = _get('playlists', {
        'part': 'id,snippet,contentDetails',
        'channelId': channel_id,
        'fields': 'items(id,snippet/title,contentDetails/itemCount)',
        'maxResults': 50,
    })
    return tuple({
        'id': item['id'],
        'title': item['snippet']['title'],
        'itemCount': item['contentDetails']['itemCount'],
    } for item in result['items'])

def get_playlist_videos(playlist_id=PLAYLIST_ID):
    """ Список видео плейлиста """
    result = _get('playlistItems', {
        'part': 'id,snippet',
        'playlistId': playlist_id,
        'fields': 'items(id,snippet/title,snippet/description,snippet/resourceId)',
        'maxResults': 50,
    })
    return tuple({
        'id': item['snippet']['resourceId']['videoId'],
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
    } for item in result['items'] if item['snippet']['resourceId']['kind'] == 'youtube#video')