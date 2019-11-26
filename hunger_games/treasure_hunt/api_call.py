import json
import requests
import time


api_token = '83efa02aa0e40572bd9b3be4978c781d02a1c55e'
api_url_base = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/'
# headers = {'Content-Type': 'application/json',
#            'Authorization': 'Token {0}'.format(api_token)}

def get_data():
    headers = {'Content-Type': 'application/json',
           'Authorization': f'Token {api_token}'}

    api_url = '{0}account/keys'.format(api_url_base + 'init/')

    response = requests.get(api_url, headers=headers)
    data = response.json()

    time.sleep(data['cooldown'])

    if response.status_code == 200:
        return data
        # return json.loads(response.content.decode('utf-8'))
    else:
        return None


def move_player(route):
    headers = {'Content-Type': 'application/json',
           'Authorization': f'Token {api_token}'}

    api_url = '{0}account/keys'.format(api_url_base + 'move/')

    response = requests.post(api_url, headers=headers, json={"direction": route})
    data = response.json()

    time.sleep(data['cooldown'])

    if response.status_code == 200:
        return data
        # return json.loads(response.content.decode('utf-8'))
    else:
        return None
