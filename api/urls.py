from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('login', views.LoginView, basename='login')
router.register('slot', views.SlotBookingView, basename='slot')
router.register('conferenceroom', views.ConferenceRoomView, basename='conferenceroom')
router.register('user', views.UserView, basename='user')

urlpatterns = [
    path('',include(router.urls))
]