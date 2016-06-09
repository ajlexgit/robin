import requests


def tinyurl(link):
    """ Минификация URL """
    response = requests.post('http://tinyurl.com/api-create.php', data={'url': link})
    return response.text

