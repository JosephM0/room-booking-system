from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer
from .permissions import IsReceptionistOrMarketing


# Create your views here.
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsReceptionistOrMarketing]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsReceptionistOrMarketing]

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = list(user.groups.values_list('name', flat=True))
        return Response({
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "groups": groups,
        })