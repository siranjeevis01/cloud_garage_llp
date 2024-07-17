import shutil
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import BarcodeForm
from .models import Barcode
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
from django.conf import settings
from django.core.files import File


class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate password criteria
        if len(password) < 6 or len(password) > 14:
            error_message = "Password must be between 6 and 14 characters long"
        elif not any(char.isupper() for char in password):
            error_message = "Password must contain at least one uppercase letter"
        elif not any(char.islower() for char in password):
            error_message = "Password must contain at least one lowercase letter"
        elif not any(char.isdigit() for char in password):
            error_message = "Password must contain at least one number"
        elif not any(char in '@$!%*?&' for char in password):
            error_message = "Password must contain at least one special character (@$!%*?&)"
        elif CustomUser.objects.filter(username=username).exists():
            error_message = "Username already exists"
        else:
            user = CustomUser.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
        
        return render(request, self.template_name, {'error_message': error_message, 'username': username})

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, self.template_name)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('login')

class BarcodeGeneratorView(View):
    template_name = 'barcode_generate.html'
    
    def get(self, request):
        form = BarcodeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BarcodeForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            folder_name = form.cleaned_data['folder_name']
            excel_path = os.path.join(settings.MEDIA_ROOT, excel_file.name)
            with open(excel_path, 'wb+') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)

            barcode_generator = BarcodeGenerator(excel_path, settings.MEDIA_ROOT, folder_name)
            barcode_generator.run()

            return redirect('success')
        return render(request, self.template_name, {'form': form})

class BarcodeGenerator:
    def __init__(self, excel_path, output_dir, folder_name):
        self.excel_path = excel_path
        self.output_dir = output_dir
        self.folder_name = folder_name
        self.new_output_dir = os.path.join(output_dir, folder_name)

    def read_excel(self):
        self.df = pd.read_excel(self.excel_path)

    def prepare_output_directory(self):
        if os.path.exists(self.new_output_dir):
            shutil.rmtree(self.new_output_dir)
        os.makedirs(self.new_output_dir, exist_ok=True)

    def generate_barcodes(self):
        for index, row in self.df.iterrows():
            barcode_number = str(row['Barcode'])
            filename = os.path.join(self.new_output_dir, f'barcode_image_{index + 1}')
            
            PRODUCT = barcode.get_barcode_class('ean13')
            product = PRODUCT(barcode_number, writer=ImageWriter())
            barcode_image_path = product.save(filename)
            
            
            with open(barcode_image_path, 'rb') as f:
                barcode_instance = Barcode(barcode_number=barcode_number)
                barcode_instance.image.save(f'barcode_image_{index + 1}.png', File(f))
                barcode_instance.save()

    def run(self):
        self.read_excel()
        self.prepare_output_directory()
        self.generate_barcodes()

class BarcodeListView(View):
    template_name = 'barcode_list.html'

    def get(self, request):
        barcodes = Barcode.objects.all()
        return render(request, self.template_name, {'barcodes': barcodes})
    
class SuccessView(View):
    template_name = 'success.html'

    def get(self, request):
        return render(request, self.template_name)
