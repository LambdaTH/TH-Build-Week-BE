import requests
import time
from decouple import config
from teleport import teleport
from api import api_request

NEW_NAME = config("NAME")


def get_current_room():
    res = api_request('/init', "GET")
    return res["room_id"]


def name_change():
    res = api_request('/change_name', "POST", {"name": NEW_NAME, "confirm": "aye"})
    return res


if __name__ == "__main__":
    current_room = get_current_room()
    name_change_room = "467"
    teleport(str(current_room), name_change_room)
    response = name_change()
    print(response)
