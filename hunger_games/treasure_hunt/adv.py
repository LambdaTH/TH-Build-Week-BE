from .api_call import move_player, get_data
from .models import Room
from .util import Queue, Stack

import random


# FILL THIS IN
# traversalPath = ['n', 's']

direction_reversed = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
traversalPath = []  # populate with n/s/e/w
# make a visited rooms set
visited = set()
# add room 0 to visited rooms
visited.add(0)
# function to traverse graph
# checks if any room around hasn't been seen
def advfunc():
    room = get_data()
    print('=====', room)
    new_room = Room(title=room['title'], id=room['room_id'], description=room['description'])
    new_room.save()
    print('+++++++', new_room)
    # currentRoomID = get_data()['room_id']
def checkRooms(currentRoomID):
    # for any_room in roomGraph[currentRoomID]:
    if room[currentRoomID] not in visited:
        return False
    else:
        return True

# function to track unvisited rooms
# goes into first unseen room around after traversing a path
def trackNewRooms(currentRoomID):
    for direction in direction_reversed:
        if move_player(direction)['room_id'] not in visited:
            visited.add(move_player(direction)['room_id'])
            new_room = Room(title=room['title'], id=room['room_id'], description=room['description'])
            new_room.save()
            traversalPath.append(direction)
            return move_player(direction)['room_id']
    print('You shall not pass!!!!')

# function to get directions
def directionToRoom(currentRoom, room):
    for path, location in roomGraph[currentRoom][1].items():
        if location == room:
            return path
    return None

# function to step back to previous rooms
def stepBackToPrev():
    q = Queue()
    visitedRoom = set()
    path = {}
    q.enqueue(currentRoom)
    path[currentRoom] = [currentRoom]
    while q.size() > 0:
        roomID = q.dequeue()
        visitedRoom.add(roomID)
        for traversedRoom in roomGraph[roomID][1].values():
            if traversedRoom in visitedRoom:
                continue
            newPath = list(path[roomID])
            newPath.append(traversedRoom)
            path[traversedRoom] = newPath
            if not checkRooms(traversedRoom):
                actualPath = path[traversedRoom]
                direction = [directionToRoom(actualPath[i], actualPath[i + 1]) for i in range(len(actualPath) - 1)]
                return (direction, actualPath[len(actualPath) - 1])
            q.enqueue(traversedRoom)
    return None
# traverse rooms using dft starting from room 0
currentRoom = 0
while True:
    while not checkRooms(currentRoom):
        currentRoom = trackNewRooms(currentRoom)
        # mark every room as seen_room
        # add it to traversal path

    # if no more rooms, loop back to the first room with other unseen rooms
    # use bfs to get from the dead end to the room with unexplored rooms if we can
    # mark every room it went throught as seen
    prevRoom = stepBackToPrev()
    # get (directions it went back through, destination room) or None
    # if can't trace back, don't add to path
    if prevRoom:
        newPath = prevRoom[0]
        traversalPath.extend(newPath)
        currentRoom = prevRoom[1]
    else:
        break


# # TRAVERSAL TEST
# visited_rooms = set()
# player.currentRoom = world.startingRoom
# visited_rooms.add(player.currentRoom)
# for move in traversalPath:
#     player.travel(move)
#     visited_rooms.add(player.currentRoom)

# if len(visited_rooms) == len(roomGraph):
#     print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
