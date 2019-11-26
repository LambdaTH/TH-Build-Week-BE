import hashlib
import requests
from decouple import config
import time

import sys

TOKEN = config("TOKEN")


def proof_of_work(last_proof, difficulty):
    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
        

    print("Proof found: " + str(proof))

    return proof


def valid_proof(last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()

    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:difficulty] == (difficulty * "0")


def mine_coin():
    base_url = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    # Get the last proof from the server
    r = requests.get(url=base_url + "/last_proof",
                     headers={"Authorization": f"Token {TOKEN}"})

    data = r.json()

    last_proof = data.get('proof')
    difficulty = data.get('difficulty')
    cool_down = data.get('cooldown')

    time.sleep(cool_down)
    coin_mined = 0
    while True:
        # Get new proof
        print('currently mining')
        
        start_time = time.time()
        new_proof = proof_of_work(last_proof, difficulty)
        end_time = time.time()
        r = requests.post(url=base_url + "/mine",
                          headers={"Authorization": f"Token {TOKEN}"},
                          json={"proof": new_proof})
        
        data = r.json()
        
        time.sleep(data['cooldown'])
        if 'New Block Forged' in data['messages']:
            print(f"Coin mined in {end_time - start_time} secs")
            coin_mined += 1
        print(data)
        print('Coin mined ', coin_mined)


if "__main__" == __name__:
    mine_coin()
