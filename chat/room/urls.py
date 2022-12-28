from django.urls import path
from room.views import views


urlpatterns = [
    path('palace', views.RoomCreateList.as_view(), name='room_list_new'),
    path('palace/<int:pk>', views.RoomUpdate.as_view(), name='room_update'),
]
