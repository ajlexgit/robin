import requests


def tinyurl(link):
    response = requests.post('http://tinyurl.com/api-create.php', data={'url': link})
    return response.text
