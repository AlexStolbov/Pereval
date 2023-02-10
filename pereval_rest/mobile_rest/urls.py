from django.urls import path
from .views import submit_data, send_data

urlpatterns = [
    path('', submit_data),
    path('<int:id>/', send_data),
]
