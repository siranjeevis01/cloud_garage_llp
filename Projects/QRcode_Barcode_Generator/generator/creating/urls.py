from django.urls import path
from .views import HomeView, RegisterView, LoginView, LogoutView, GeneratedView, OutputGeneratedView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate/', GeneratedView.as_view(), name='generate'),
    path('generated-output/', OutputGeneratedView.as_view(), name='success'),  
]
