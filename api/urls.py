from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterCustoUser.as_view())
]
