from requests import request
from .serializers import *
from .models import *
import re


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from drf_yasg.utils import swagger_auto_schema

from helper import validate_email, hash_password, check_password
from django.db.models import F

class UserView(viewsets.ViewSet):
    #get user by id
    @swagger_auto_schema(
        operation_description="Get user by id",
        responses={
            200: UserSerializer
        }
    )
    def retrieve(self, request, pk=None):
        try:
            user_qs = User.objects.filter(id=pk)
            if not user_qs:
                return Response({
                    "msg": "No users found", 
                    "status":status.HTTP_404_NOT_FOUND
                    },status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user_qs[0])
            return Response({
                "msg": "success",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Create user",
        request_body=UserSerializer,
        responses={
            201: UserSerializer
        }
    )
    def create(self, request):
        '''
        POST request with Body
            {                
                    "name":"ankit",
                    "email":"ankit@tradeindia.com",
                    "password":"1234"
            }
        '''
        try:
            if not validate_email(request.data['email']):
                return Response({
                    "msg": "Invalid email",
                    "status": status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)
            request.data['password'] = hash_password(request.data['password']).decode('utf-8')
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "success",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED
                },status=status.HTTP_201_CREATED)
            return Response({
                "msg": "failed",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(viewsets.ViewSet):
    
    @swagger_auto_schema(
        operation_description="Login user",
        request_body=LoginUserSerializer,
        responses={
            200: LoginSerializer
        }
    )
    def create(self, request):
        try:
            user_qs = User.objects.filter(email=request.data['email'])
            if not user_qs:
                return Response({
                    "msg": "No users found",
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            if check_password(request.data['password'], user_qs[0].password):
                serializer = LoginSerializer(user_qs[0])
                return Response({
                    "msg": "success",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            return Response({
                "msg": "Invalid password",
                "status": status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

class ConferenceRoomView(viewsets.ViewSet):
    #get all conference rooms
    @swagger_auto_schema(responses={200: ConferenceroomSerializer(many=True)})
    def list(self, request,id=None, format=None):
        try:
            conf_room_qs = Conferenceroom.objects.all()
            if not conf_room_qs:
                return Response({
                    "msg": "No conference rooms found",
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            serializer = ConferenceroomSerializer(conf_room_qs, many=True)
            return Response({
                "msg": "success",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(responses={200: ConferenceroomSerializer(many=True)})
    def retrive(self, request, id):
        try:
            conf_room_qs = Conferenceroom.objects.get(id=id)
            if not conf_room_qs:
                return Response({
                    "msg": "No conference rooms found",
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            serializer = ConferenceroomSerializer(conf_room_qs)
            return Response({
                "msg": "success",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)

        
    #create a conference room
    @swagger_auto_schema(request_body=ConferenceroomSerializer)
    def create(self, request):
        '''
        POST request with Body
            {
                "name":"Bluemoon",
                "is_active":true,
                "projector":true,
                "white_board":true,
                "capacity":20,
                "description":"conference room have a capacity of 20 person"
            }
        '''
        try:
            serializer = ConferenceroomSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "success",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED
                },status=status.HTTP_201_CREATED)
            return Response({
                "msg": "failed",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #update a conference room
    @swagger_auto_schema(request_body=ConferenceroomSerializer)
    def update(self, request, pk=None):
        '''
        PUT request with Body
            {
                "name":"Bluemoon",
                "is_active":true,
                "projector":true,
                "white_board":true,
                "capacity":20,
                "description":"conference room have a capacity of 20 person"
            }
        '''
        try:
            conf_room_qs = Conferenceroom.objects.get(id=pk)
            serializer = ConferenceroomSerializer(conf_room_qs, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "success",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            return Response({
                "msg": "failed",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)
    
    #delete a conference room
    def destroy(self, request, pk=None):
        try:
            conf_room_qs = Conferenceroom.objects.get(id=pk)
            conf_room_qs.delete()
            return Response({
                "msg": "success",
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)


class SlotBookingView(viewsets.ViewSet):
    #get all slot bookings with user and conference room
    @swagger_auto_schema(responses={200: BookingslotsSerializer(many=True)})
    def list(self, request):
        try:
            slot_booking_qs = Bookingslots.objects.annotate(book_date=F('booking_date')).all().order_by('book_date')
            if not slot_booking_qs:
                return Response({
                    "msg": "No slot bookings found",
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            serializer = BookingslotsSerializer(slot_booking_qs, many=True)
            return Response({
                "msg": "success",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)
    
    #get a slot by id
    @swagger_auto_schema(responses={200: BookingslotsSerializer(many=True)})
    def retrieve(self, request, pk=None):
        try:
            slot_booking_qs = Bookingslots.objects.get(id=pk)
            if not slot_booking_qs:
                return Response({
                    "msg": "No slot bookings found",
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            serializer = BookingslotsSerializer(slot_booking_qs)
            return Response({
                "msg": "success",
                "data": serializer.data,
                "status": status.HTTP_200_OK
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)

    #create a slot booking
    @swagger_auto_schema(request_body=BookingslotsCreateSerializer)
    def create(self, request):
        try:
            conf_id = request.data['conference_room']
            user_id = request.data['user']
            try:
                conf_room_qs = Conferenceroom.objects.get(id=conf_id)
                user_qs = User.objects.get(id=user_id)
                
            except Exception as e:
                return Response({
                    "msg": re.sub(' matching query', '',str(e)),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            
            from_time = request.data['start_time']
            to_time = request.data['end_time']
            book_date = request.data['booking_date']
        
            slot_qs = Bookingslots.objects.filter(start_time__range=(from_time, to_time), end_time__range=(from_time,to_time),booking_date=book_date ,conference_room=conf_room_qs)

            if slot_qs:
                return Response({
                    "msg": "Slot already booked for this conference room",
                    "status": status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)

            serializer = BookingslotsCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "success",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            return Response({
                "msg": "failed",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)
    
    #update a slot booking
    @swagger_auto_schema(request_body=BookingslotsCreateSerializer)
    def update(self, request, pk=None):
        try:
            conf_id = request.data.get('conference_room')
            user_id = request.data.get('user')
            try:
                conf_room_qs = Conferenceroom.objects.get(id=conf_id)
                user_qs = User.objects.get(id=user_id)
                
            except Exception as e:
                print('erer ',e)
                return Response({
                    "msg": re.sub(' matching query', '',str(e)),
                    "status": status.HTTP_404_NOT_FOUND
                },status=status.HTTP_404_NOT_FOUND)
            
            from_time = request.data.get('start_time')
            to_time = request.data.get('end_time')
            book_date = request.data.get('booking_date')
        
            slot_qs = Bookingslots.objects.filter(start_time__range=(from_time, to_time), end_time__range=(from_time,to_time),booking_date=book_date ,conference_room=conf_room_qs)

            if slot_qs:
                return Response({
                    "msg": "Slot already booked for this conference room",
                    "status": status.HTTP_400_BAD_REQUEST
                },status=status.HTTP_400_BAD_REQUEST)

            slot_booking_qs = Bookingslots.objects.get(id=pk)
            serializer = BookingslotsSerializer(slot_booking_qs, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "success",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK
                },status=status.HTTP_200_OK)
            return Response({
                "msg": "failed",
                "data": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "msg": str(e),
                "status": status.HTTP_404_NOT_FOUND
            },status=status.HTTP_404_NOT_FOUND)