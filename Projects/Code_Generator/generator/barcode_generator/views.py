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
            excel_files = request.FILES.getlist('excel_file')
            folder_name = form.cleaned_data['folder_name']
            
            media_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
            os.makedirs(media_dir, exist_ok=True)
            
            try:
                for excel_file in excel_files:
                    excel_path = os.path.join(media_dir, excel_file.name)
                    
                    with open(excel_path, 'wb+') as destination:
                        for chunk in excel_file.chunks():
                            destination.write(chunk)
                    
                    print(f"Excel file saved at: {excel_path}")
                    
                    barcode_generator = BarcodeGenerator(excel_path, settings.MEDIA_ROOT, folder_name)
                    barcode_generator.run()
                    print(f"Barcodes generated for {excel_file.name}")
                
                messages.success(request, 'Barcodes generated successfully.')
                return redirect('success')
            
            except Exception as e:
                messages.error(request, f"Error generating barcodes: {e}")
                print(f"Error generating barcodes: {e}")
        
        return render(request, self.template_name, {'form': form})

class BarcodeGenerator:
    def __init__(self, excel_path, output_dir, folder_name):
        self.excel_path = excel_path
        self.output_dir = output_dir
        self.folder_name = folder_name
        self.new_output_dir = os.path.join(output_dir, 'barcodes', folder_name)
        self.save_last_generated_folder()

    def read_excel(self):
        self.df = pd.read_excel(self.excel_path)
        print("DataFrame columns:", self.df.columns)  
        print("DataFrame head:", self.df.head())  
        
        expected_columns = ['Barcode']
        actual_columns = list(self.df.columns) 
        if actual_columns and isinstance(actual_columns[0], int):
            actual_columns = ['Barcode' if i == 0 else str(i) for i in range(len(actual_columns))]
            self.df.columns = actual_columns
        if 'Barcode' not in self.df.columns:
            raise KeyError("Column 'Barcode' not found in Excel file.")

    def prepare_output_directory(self):
        if os.path.exists(self.new_output_dir):
            shutil.rmtree(self.new_output_dir)
        os.makedirs(self.new_output_dir, exist_ok=True)

    def generate_barcodes(self):
        try:
            for index, row in self.df.iterrows():
                barcode_number = str(row['Barcode'])
                print(f"Generating barcode for: {barcode_number}") 
                filename = os.path.join(self.new_output_dir, f'barcode_image_{index + 1}.png')
                
                PRODUCT = barcode.get_barcode_class('ean13')
                product = PRODUCT(barcode_number, writer=ImageWriter())
                barcode_image_path = product.save(filename)
                print(f"Barcode image saved at: {barcode_image_path}")
                
                
        except KeyError as e:
            print(f"KeyError: {e}")

        except Exception as e:
            print(f"Error generating barcodes: {e}")

    def save_last_generated_folder(self):
        with open(os.path.join(self.output_dir, 'last_generated_folder.txt'), 'w') as f:
            f.write(self.folder_name)

    def run(self):
        self.read_excel()
        self.prepare_output_directory()
        self.generate_barcodes()


class LastBarcodeGeneratedListView(View):
    template_name = 'last_barcode_generated_list.html'

    def get(self, request):
        folder_name = self.get_last_generated_folder_name()
        if folder_name:
            folder_path = os.path.join(settings.MEDIA_ROOT, 'barcodes', folder_name)
            images = []
            if os.path.exists(folder_path):
                images = [
                    os.path.join(settings.MEDIA_URL, 'barcodes', folder_name, file)
                    for file in os.listdir(folder_path)
                    if file.endswith('.png')
                ]
        else:
            images = []

        return render(request, self.template_name, {'folder_name': folder_name, 'images': images})

    def get_last_generated_folder_name(self):
        try:
            with open(os.path.join(settings.MEDIA_ROOT, 'last_generated_folder.txt'), 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

class BarcodeListView(View):
    template_name = 'barcode_list.html'

    def get(self, request):
        folders = Barcode.objects.values_list('folder_name', flat=True).distinct()
        return render(request, self.template_name, {'folders': folders})
    
class SuccessView(View):
    template_name = 'success.html'

    def get(self, request):
        return render(request, self.template_name)