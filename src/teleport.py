import json
import requests
from decouple import config
from time import sleep
import argparse
from utils import Queue, Stack
from api import api_request


def directionToRoom(room_map, currentRoomID, room_id):
    for d, r in room_map[currentRoomID].items():
        if r == room_id:
            return d
    return None

def find_path(room_map, room_details, currentRoomID, destinationRoomName):
    visited = set()
    paths = {}
    q = Queue()
    q.enqueue(currentRoomID)
    paths[currentRoomID] = [currentRoomID]
    while q.size() > 0:
        room = q.dequeue()
        visited.add(room)
        for searched_room_id in room_map[room].values():
            if searched_room_id in visited or searched_room_id == '?':
                continue
            newPath = paths[room][:]
            newPath.append(searched_room_id)
            paths[searched_room_id] = newPath
            room_found = False
            for room_info in room_details:
                if searched_room_id == str(room_info['room_id']):
                    if room_info['title'].lower() == destinationRoomName.lower():
                        room_found = True
                        break
                    if 'items' in room_info and destinationRoomName in room_info['items']:
                        room_found = True
                        break
            if searched_room_id == destinationRoomName:
                room_found = True
            if room_found:
                actualPath = paths[searched_room_id]
                directions = [directionToRoom(room_map, actualPath[i], actualPath[i + 1]) for i in range(len(actualPath) - 1)]
                return directions
            q.enqueue(searched_room_id)
    return None


def teleport(currentRoomID, destination_room_id):
    room_details = []
    room_map = {}
    with open("room_details.py", "r") as f:
        room_details = json.loads(f.read())
    with open("room_graph.py", "r") as f:
        room_map = json.loads(f.read())
    # Traverse the map to find the path
    path = find_path(room_map, room_details, currentRoomID, destination_room_id)
    print(f"FOLLOW THIS PATH {path} TO ROOM {destination_room_id}")
    # If path not found, print "path to {destination_room_id} not found"
    if not path:
        print(f"path to {destination_room_id} not found")
        return
    # If path found, go through each room to the destination room
    for i in range(len(path)):
        next_room_id = room_map[currentRoomID][path[i]]
        data = api_request('/move', "POST", {
                "direction": path[i], "next_room_id": next_room_id})

        print(data)
        currentRoomID = str(data['room_id'])


def get_current_room():
    # make request to the init endpoint
    response = api_request('/init', "GET")

    # get room id
    room_id = response["room_id"]

    # return the room_id in string format
    return str(room_id)


if __name__ == "__main__":
    # instantiate the argument parser
    parser = argparse.ArgumentParser()

    # add the filename argument to the parser
    parser.add_argument("destination")

    # parse to get the argument
    args = parser.parse_args()

    # get the player's current room
    current_room = get_current_room()

    # get the destination room
    destination = args.destination

    # call teleport with the arg and current room
    teleport(current_room, destination)
