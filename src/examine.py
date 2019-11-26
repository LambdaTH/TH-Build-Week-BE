import requests
from decouple import config
from api import api_request
import argparse

def examine_room(currentRoom=None, playerName=None):
    options = {}
    if currentRoom == 55:
        playerName = "WELL"
    options["name"]= playerName
    response = api_request('/examine', "POST" , options)
    if response['name'] == 'Wishing Well':
        with open("wishing_well_prophecy.txt", "w") as f:
            f.write(response["description"])

if __name__ == "__main__":
    currentRoom =  api_request('/init', "GET")
     # instantiate the argument parser
    parser = argparse.ArgumentParser()

    # add the filename argument to the parser
    parser.add_argument("PlayerName")

    # parse to get the argument
    args = parser.parse_args()

    # get the destination room
    PlayerName = args.PlayerName

    # call teleport with the arg and current room
    # teleport(current_room, destination)
    response = examine_room(currentRoom['room_id'], PlayerName)
    print(response)