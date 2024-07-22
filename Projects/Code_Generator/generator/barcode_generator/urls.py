from django.urls import path
from .views import RegisterView, LoginView, LogoutView, BarcodeGeneratorView, HomeView, BarcodeListView, SuccessView, LastBarcodeGeneratedListView, QRCodeGeneratorView, LastQRCodeGeneratedListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('generate-barcode/', BarcodeGeneratorView.as_view(), name='generate_barcode'),
    path('barcodes/', BarcodeListView.as_view(), name='barcode_list'),
    path('', HomeView.as_view(), name='home'),  
    path('success/', SuccessView.as_view(), name='success'),
    path('last_barcode_generated_list/', LastBarcodeGeneratedListView.as_view(), name='last_barcode_generated_list'),
    path('qr-code/generate/', QRCodeGeneratorView.as_view(), name='qr_code_generate'),
    path('qr-code/last/', LastQRCodeGeneratedListView.as_view(), name='last_qr_code_generated_list'),
]