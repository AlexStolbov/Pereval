from django.urls import path
from .views import submit_data

urlpatterns = [
    path('', submit_data),
]
