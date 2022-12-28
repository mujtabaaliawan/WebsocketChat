from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('token', TokenObtainPairView.as_view(), name='token_new'),
    path('token-refresh', TokenRefreshView.as_view(), name='token_update'),
    path('', include('user.urls')),
    path('', include('chatter.urls')),
    path('', include('room.urls')),
    path('', include('box.urls')),
    path('', include('message.urls')),
]
