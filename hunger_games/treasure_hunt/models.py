from django.db import models

class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=-1)
    s_to = models.IntegerField(default=-1)
    e_to = models.IntegerField(default=-1)
    w_to = models.IntegerField(default=-1)
    x = models.IntegerField(default=-1)
    y = models.IntegerField(default=-1)

    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()





