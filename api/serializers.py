from rest_framework import serializers
from .models import Conferenceroom, User, Bookingslots

# create a conference room serializer
class ConferenceroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conferenceroom
        fields = '__all__'

#User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#Booking serializer
class BookingslotsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name')
    conference_room_name = serializers.CharField(source='conference_room.name')
    class Meta:
        model = Bookingslots
        fields = '__all__'

#Booking serializer for create request
class BookingslotsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookingslots
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email']

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']