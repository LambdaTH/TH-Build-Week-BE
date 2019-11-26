import requests
from decouple import config
import time

url = "https://lambda-treasure-hunt.herokuapp.com/api/adv"
token = config('TOKEN')

def api_request(route, verb, option=None):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Token {token}'}
    
    response = None

    if verb == 'GET':
      response = requests.get(f"{url}{route}", headers=headers)
    if verb == 'POST':
      response = requests.post(f"{url}{route}", headers=headers, json=option)
    
    data = response.json()
    time.sleep(data["cooldown"])


    return data