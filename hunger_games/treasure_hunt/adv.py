from .api_call import move_player, get_data
from .models import Room
from .util import Queue, Stack

import random
import json

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'room_graph.py')
my_file2 = os.path.join(THIS_FOLDER, 'room_details.py')




# cache room map
room_map = {}

# cache room details
room_details = []

traversalPath = []  # populate with n/s/e/w

# function to traverse graph
# checks if any room around hasn't been seen
def advfunc():
    # room = get_data()
    # move = move_player('n')
    # print('=====', room)
    # print('*************', move)
    # new_room = Room(title=room['title'], id=room['room_id'], description=room['description'])
    # new_room.save()
    # print('+++++++', new_room)
    with open(my_file, "r") as f:
    # read the map from room_graph file
        room_map = json.loads(f.read())

    with open(my_file2, "r") as f:
    # read the map from room_details file
        room_details = json.loads(f.read())

# get players current room which is the last room in room details
    currentRoomID = room_details[-1]['room_id']

# get opposite directions
    reverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

# function to track unvisited rooms
# goes into first unseen room around after traversing a path
    def trackNewRooms(queue):
        """Finds the next unexplored room in the players current room
        and adds it to the queue.

        Arguments:
        player {class} -- instance of the Player class
        queue {class} -- instance of the Queue class
        """
        currentRoomID = str(room_details[-1]['room_id'])

        # get exists in current room
        currentRoom = room_map[currentRoomID]
        # cache unvisited paths
        unvisited_paths = []
    
    #loop through current room
        for d in currentRoom:
            if currentRoom[d] == '?':
            # add to unvisited path
                unvisited_paths.append(d)
            # print('You shall not pass!!!!')
    # if there are unvisted rooms
        if unvisited_paths:
        # add first room to queue
            queue.enqueue(unvisited_paths[0])
        else:
        # trace back abd find other rooms
            unvisited_path = stepBackToPrev()

        # if there are unvisited rooms
            if unvisited_path is not None:
            # loop through the unvisited paths
                for path in unvisited_path:
                # check exits in current room
                    for exit in currentRoom:
                    # if path is in current room, enqueue
                        if currentRoom[exit] == path:
                            queue.enqueue(exit)


# function to step back to previous rooms
    def stepBackToPrev():
        """Uses bft to find the path to the closest room with an unexplored
        direction. When it finds one it returns the path. Returns None
        when an unexplored direction can not be found

        Arguments:
            player {class} -- instance of the Player class

        Returns:
            list -- path to the room with an unexplored direction
        """
        q = Queue()
        visitedRoom = set()
    # enqueue the current room as a list
        q.enqueue([currentRoomID])
        while q.size() > 0:
        # get the rooms
            room_set = q.dequeue()
         # grab the last room
            last_room = room_set[-1]

            if last_room not in visitedRoom:
                visitedRoom.add(room_set)
            for exit in room_map[last_room]:
            # if unvisited, return the current room
                if room_map[last_room][exit] == '?':
                    return room_set
                else:
                    newPath = list(room_set)
                    newPath.append(room_map[last_room][exit])
                    # enque the new path
                    q.enqueue(newPath)
        return None

# create queue
    q = Queue()

# call get_unexplored_room with queue and player
    trackNewRooms(q)

# while there is still an unexplored room
    while q.size() > 0:
        with open(my_file, "r") as f:
    # read the map from room_graph file
            room_map = json.loads(f.read())

        with open(my_file2, "r") as f:
    # read the map from room_details file
            room_details = json.loads(f.read())

    # current players position
        current_player_position = str(room_details[-1]["room_id"])

    # the next direction
        next_direction = q.dequeue()


    # move the player in that direction
        # move_player(next_direction)

    # add it to the traversal path
        traversalPath.append(next_direction)

    # get the response
        data = move_player(next_direction)
        print('*************', data)
        # load rooms to database
        new_room = Room(title=data['title'], id=data['room_id'], description=data['description'])
        # new_room.save()
        print('+++++++', new_room)

    # set the player's destination room
    # add it to the room_datails
        room_details.append(data)

    # new player position
        destination_room = str(room_details[-1]["room_id"])

    # update the map with the new discovery
        room_map[current_player_position][next_direction] = destination_room

    # if the current room has not been added to the map
        if destination_room not in room_map:
            exits = data["exits"]
            directions = {}

            for d in exits:
                directions[d] = "?"

        # add it and set to empty dictionary
            room_map[destination_room] = directions

    # get reverse direction to set it in the previous room
        r_direction = reverse_directions[next_direction]
    # point the destination room to the previous room
        room_map[destination_room][r_direction] = current_player_position

    # write the new changes to the file
        with open(my_file, "w") as f:
            f.write(json.dumps(room_map))

        with open(my_file2, "w") as f:
            f.write(json.dumps(room_details))


    # call get_unexplored_room to add the next direction to the queue
        trackNewRooms(q)
