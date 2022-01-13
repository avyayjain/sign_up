from django.urls import path
from . import views

urlpatterns = [
    path('operation/', views.OperationUser),
    path('client/', views.ClientUser),
    path('login/', views.login),
    path('status-client/', views.statusclient),
    path('logout/', views.logout),
]
