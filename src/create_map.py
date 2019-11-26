import json
from utils import Queue, Stack
from api import api_request

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'room_graph.py')
my_file2 = os.path.join(THIS_FOLDER, 'room_details.py')


traversalPath = []

reverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

traversalGraph = {}
room_details = []

stack = Stack()
prev_room = None
prev_cardinal = None

currentRoom_data = api_request('/init', "GET")

while len(traversalGraph) < 500:
    currentRoom = currentRoom_data['room_id']
    print(currentRoom_data)

    # write the new changes to the file
    # with open(my_file, "w") as f:
    #     f.write(json.dumps(traversalGraph))

    # with open(my_file2, "w") as f:
    #     f.write(json.dumps(room_details))

    if str(currentRoom) == '22' or str(currentRoom) == '461':
        print('you just prayed')
        api_request('/pray', "POST")

    if len(currentRoom_data['items']) > 0:
        inventory = api_request('/status', "POST")
        if inventory['strength'] > inventory['encumbrance']:
            for item in currentRoom_data['items']:
                api_request('/take', "POST", {"name": item})
                print(f"picked up item - {item}")

    if str(currentRoom) == '1':
        inventory = api_request('/status', "POST")
        if len(inventory['inventory']) > 0:
            for item in inventory['inventory']:
                api_request('/sell', "POST", {"name": item,  "confirm": "yes"})
                print(f"sold {item}")

    if currentRoom not in traversalGraph:
        room_details.append(currentRoom_data)
        exits = {direction: '?' for direction in currentRoom_data['exits']}
        traversalGraph[currentRoom] = exits

    if prev_room:
        traversalGraph[prev_room][prev_cardinal] = currentRoom
        reverse_cardinal = reverse_directions[prev_cardinal]
        traversalGraph[currentRoom][reverse_cardinal] = prev_room
    prev_room = currentRoom

    movement = False
    for exit_cardinal, room in traversalGraph[currentRoom].items():
        if room == "?":
            prev_cardinal = exit_cardinal
            stack.push(exit_cardinal)
            traversalPath.append(exit_cardinal)
            currentRoom_data = api_request(
                '/move', "POST", {"direction": exit_cardinal})
            movement = True
            break

    if not movement:
        exit_cardinal = reverse_directions[stack.pop()]
        traversalPath.append(exit_cardinal)
        prev_cardinal = exit_cardinal
        currentRoom_data = api_request(
            '/move', "POST", {"direction": exit_cardinal})
