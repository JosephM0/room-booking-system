from rest_framework import serializers
from .models import Room, Booking
from django.db.models import Q

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        room = data.get('room')

        if start_date > end_date:
            raise serializers.ValidationError("Start date cannot be after end date.")
        
        overlapping = Booking.objects.filter(
            room = room
        ).filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        )

        if self.instance:
            overlapping = overlapping.exclude(id=self.instance.id)

        if overlapping.exists():
            raise serializers.ValidationError(
                f"{room.name} is already booked for those dates."
            )
        
        return data