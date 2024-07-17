from django.urls import path
from .views import RegisterView, LoginView, LogoutView, BarcodeGenerateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate-barcodes/', BarcodeGenerateView.as_view(), name='generate_barcodes'),
]
