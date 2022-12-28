from django.urls import path
from chatter.views import views


urlpatterns = [
    path('chatter', views.ChatterCreateList.as_view(), name='chatter_list_new'),
    path('chatter/<int:pk>', views.ChatterUpdate.as_view(), name='chatter_update'),
]
