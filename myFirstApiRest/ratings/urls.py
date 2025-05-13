from django.urls import path
from .views import RatingListCreate, RatingRetrieveUpdateDestroy

urlpatterns = [
    path('', RatingListCreate.as_view(), name='rating-list-create'),
    path('<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-detail'),
]