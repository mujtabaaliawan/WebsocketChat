from django.urls import path
from box.views import views


urlpatterns = [
    path('box', views.BoxCreateList.as_view(), name='box_list_new'),
    path('box/<int:pk>', views.BoxUpdate.as_view(), name='box_update'),
    path('induction/<int:pk>', views.InductionUpdate.as_view(), name='induction'),
    path('detail/<int:box_id>', views.BoxDetail.as_view(), name='box_detail'),
]
