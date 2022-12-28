from django.urls import path
from user.views import views


urlpatterns = [
    path('user', views.UserList.as_view(), name='user_list_new'),
    path('user/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
]