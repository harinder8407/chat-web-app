from django.urls import path
from django.conf.urls import url
from .views import index, room, logout

app_name = 'chat'
urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('logout/', logout, name='logout'),
    
]
