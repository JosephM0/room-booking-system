from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.guest_name} - {self.room.name}"