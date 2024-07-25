from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.studentApi),
    path('students/<int:id>/', views.studentApi),
]
