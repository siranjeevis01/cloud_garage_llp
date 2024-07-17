from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import os
import shutil
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect('login')


class BarcodeGenerateView(LoginRequiredMixin, View):
    template_name = 'barcode_generate.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        excel_file = request.FILES.get('excel_file')
        output_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        folder_name = request.POST.get('folder_name', 'barcodes')

        excel_path = os.path.join(output_dir, 'barcodes.xlsx')
        with open(excel_path, 'wb') as f:
            for chunk in excel_file.chunks():
                f.write(chunk)

        generator = BarcodeGenerator(excel_path, output_dir, folder_name)
        generator.run()

        barcode_images = os.listdir(generator.new_output_dir)
        return render(request, self.template_name, {'barcode_images': barcode_images})
