from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('user-information/<slug:query_type>', GetUser.as_view())
]
