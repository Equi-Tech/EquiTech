# urls.py (inside your app or project)
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.fingerprint_login, name='fingerprint_login'),
]
