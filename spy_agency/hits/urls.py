from django.urls import path

from .views import HitList, HitUpdate, CreateHit, BulkHits


app_name = 'hits'

urlpatterns = [
    path('', HitList.as_view(), name='list'),
    path('<int:pk>/', HitUpdate.as_view(), name='update'),
    path('create/', CreateHit.as_view(), name='create'),
    path('bulk/', BulkHits.as_view(), name='bulk'),
    ]
