from django.db import models

class Conferenceroom(models.Model):
    name = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    vacant = models.BooleanField(default=True)
    projector = models.BooleanField(default=False)
    white_board = models.BooleanField(default=True)
    capacity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bookingslots(models.Model):
    is_available = models.BooleanField(default=True, db_column='is_active')
    meet_agenda = models.TextField(blank=True, null=True)
    booking_date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conference_room = models.ForeignKey('Conferenceroom', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
