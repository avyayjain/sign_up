from django.urls import path
from . import views

urlpatterns = [
    path('operation/', views.OperationUser),
    path('client/', views.ClientUser),
    path('login/', views.login),
    path('user/', views.getdata),
    path('logout/', views.logout),
]
