import requests
from django.conf import settings

API_URL = 'https://www.googleapis.com/youtube/v3/'
API_KEY = getattr(settings, 'YOUTUBE_APIKEY', 'AIzaSyB4CphiSoXhku-rP9m5-QkXE9U11OJkOzg')


def _get(resource, data):
    default = {
        'key': API_KEY,
    }
    default.update(data)

    url = '%s%s' % (API_URL, resource)
    response = requests.get(url, params=default)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError('API response: %s' % response.status_code)


def get_channel_info(channel_id):
    """ Информация о канале """
    result = _get('channels', {
        'id': channel_id,
        'part': 'snippet,contentDetails',
        'fields': 'items(snippet/title,snippet/description,snippet/thumbnails,contentDetails/relatedPlaylists/uploads)',
    })

    try:
        item = result['items'][0]
    except KeyError:
        return {}

    return {
        'id': channel_id,
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'thumbnails': item['snippet']['thumbnails'],
        'uploads': item['contentDetails']['relatedPlaylists']['uploads'],
    }


def get_channel_playlists(channel_id, per_page=20, next_page_token=''):
    """ Список плейлистов канала """
    result = _get('playlists', {
        'channelId': channel_id,
        'part': 'snippet,contentDetails',
        'fields': 'items(id,snippet/title,contentDetails/itemCount),pageInfo/*,nextPageToken',
        'pageToken': next_page_token,
        'maxResults': per_page,
    })

    return {
        'total': result['pageInfo']['totalResults'],
        'next_page_token': result.get('nextPageToken', ''),
        'items': tuple({
            'id': item['id'],
            'title': item['snippet']['title'],
            'itemCount': item['contentDetails']['itemCount'],
        } for item in result['items']),
    }


def get_playlist_videos(playlist_id, per_page=50, next_page_token=''):
    """ Список видео плейлиста """
    result = _get('playlistItems', {
        'part': 'snippet',
        'playlistId': playlist_id,
        'fields': 'items(id,snippet/title,snippet/description,snippet/thumbnails,snippet/position,snippet/resourceId),pageInfo/*,nextPageToken',
        'pageToken': next_page_token,
        'maxResults': per_page,
    })

    return {
        'total': result['pageInfo']['totalResults'],
        'next_page_token': result.get('nextPageToken', ''),
        'items': tuple({
            'id': item['snippet']['resourceId']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'thumbnails': item['snippet']['thumbnails'],
            'position': item['snippet']['position'],
        } for item in result['items'] if item['snippet']['resourceId']['kind'] == 'youtube#video'),
    }


def get_video_info(video_id):
    """ Информация о видео """
    result = _get('videos', {
        'id': video_id,
        'part': 'snippet,player',
        'fields': 'items(snippet/title,snippet/description,snippet/thumbnails,player/embedHtml)',
    })

    try:
        item = result['items'][0]
    except KeyError:
        return {}

    return {
        'id': video_id,
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'thumbnails': item['snippet']['thumbnails'],
        'embed': item['player']['embedHtml'],
    }
