from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import CustomUser
import os
import shutil
import pandas as pd
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from barcode.writer import ImageWriter
import barcode
import qrcode
from PIL import Image
from .forms import BarcodeForm

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
        error_message = None

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

class GeneratedView(View):
    template_name = 'code_generate.html'

    def get(self, request):
        form = BarcodeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BarcodeForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            folder_name = form.cleaned_data['folder_name']
            media_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
            os.makedirs(media_dir, exist_ok=True)

            try:
                excel_path = os.path.join(media_dir, excel_file.name)
                with open(excel_path, 'wb+') as destination:
                    for chunk in excel_file.chunks():
                        destination.write(chunk)

                barcode_generator = Generator(excel_path, media_dir, folder_name)
                barcode_generator.run()

                messages.success(request, 'Barcodes and QR codes generated successfully.')
                return redirect('success')

            except Exception as e:
                messages.error(request, f"Error generating barcodes and QR codes: {e}")

        return render(request, self.template_name, {'form': form})

class Generator:
    def __init__(self, excel_path, output_dir, folder_name):
        self.excel_path = excel_path
        self.output_dir = output_dir
        self.folder_name = folder_name
        self.new_output_dir = os.path.join(output_dir, folder_name)
        self.save_last_generated_folder()

    def save_last_generated_folder(self):
        if os.path.exists(self.new_output_dir):
            shutil.rmtree(self.new_output_dir)
        os.makedirs(self.new_output_dir, exist_ok=True)

    def read_excel(self):
        self.df = pd.read_excel(self.excel_path)
        required_columns = ['Barcode', 'ID', 'Name', 'Email', 'Phone Number', 'Course Title', 'Course Framework', 'Start Date', 'Amount']
        for col in required_columns:
            if col not in self.df.columns:
                raise KeyError(f"Column '{col}' not found in Excel file.")

    def generate_barcodes_and_qrcodes(self):
        try:
            for index, row in self.df.iterrows():
                barcode_number = str(row['Barcode'])
                qr_code_data = f"ID: {row['ID']}\nName: {row['Name']}\nEmail: {row['Email']}\nPhone Number: {row['Phone Number']}\nCourse Title: {row['Course Title']}\nCourse Framework: {row['Course Framework']}\nStart Date: {row['Start Date']}\nAmount: {row['Amount']}"
                filename = os.path.join(self.new_output_dir, f'image_{index + 1}.png')

                barcode_img = self.create_barcode_image(barcode_number)
                qr_code_img = self.create_qr_code_image(qr_code_data)
                combined_img = self.combine_images(barcode_img, qr_code_img)

                combined_img.save(filename)

        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"Error generating barcodes and QR codes: {e}")

    def create_barcode_image(self, barcode_number):
        PRODUCT = barcode.get_barcode_class('ean13')
        product = PRODUCT(barcode_number, writer=ImageWriter())
        barcode_image = product.render()
        return barcode_image

    def create_qr_code_image(self, qr_code_data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')
        return qr_img

    def combine_images(self, barcode_img, qr_code_img):
        qr_code_img = qr_code_img.resize((100, 100))

        combined_width = barcode_img.width + qr_code_img.width
        combined_height = max(barcode_img.height, qr_code_img.height)
        combined_img = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))

        combined_img.paste(barcode_img, (0, 0))
        combined_img.paste(qr_code_img, (barcode_img.width, 0))

        return combined_img

    def run(self):
        self.read_excel()
        self.generate_barcodes_and_qrcodes()

class OutputGeneratedView(View):
    template_name = 'output_generated.html'

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
        barcodes_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        if os.path.exists(barcodes_dir):
            return max(
                [d for d in os.listdir(barcodes_dir) if os.path.isdir(os.path.join(barcodes_dir, d))],
                key=lambda d: os.path.getmtime(os.path.join(barcodes_dir, d))
            )
        return None
