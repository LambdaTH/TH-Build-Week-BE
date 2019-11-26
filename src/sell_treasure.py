from api import api_request
from teleport import teleport

def sell_treasure():
	currentRoom = str(api_request("/init", "GET")["room_id"])
	
	if currentRoom != '1':
		print("We're going to the shop first")
		teleport(currentRoom, '1')
	
	if currentRoom == '1':
		inventory = api_request('/status', "POST")
		if len(inventory['inventory']) > 0:
			for item in inventory['inventory']:
				api_request('/sell', "POST", {"name": item,  "confirm": "yes"})
				print(f"sold {item}")
		else:
			print("You don't have anything to sell")

if __name__ == "__main__":
	sell_treasure()