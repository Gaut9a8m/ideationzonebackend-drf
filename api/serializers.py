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
    class Meta:
        model = Bookingslots
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email']