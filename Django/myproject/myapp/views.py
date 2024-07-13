from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

class UserAuthViews:
    @staticmethod
    def register(request):
        if request.method == 'POST':
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
            elif User.objects.filter(username=username).exists():
                error_message = "Username already exists"
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('login')
    
            return render(request, 'register.html', {'error_message': error_message, 'username': username, 'password': password})
        
        return render(request, 'register.html')

    @staticmethod
    def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                return redirect('home')
            else:
                return HttpResponse("Invalid credentials")
        return render(request, 'login.html')

    @staticmethod
    def home(request):
        username = request.session.get('username', 'Guest')
        visit_count = request.session.get('visit_count', 0)  
        visit_count += 1  
        request.session['visit_count'] = visit_count  
        
        return render(request, 'home.html', {'username': username, 'visit_count': visit_count})


    @staticmethod
    def logout(request):
        logout(request)
        request.session.flush()
        return redirect('login')
    
user_auth_views = UserAuthViews()


class SessionCookieViews:
    @staticmethod
    def set_session(request):
        request.session['username'] = 'Siranjeevis'
        request.session['email'] = 'siranjeevis@gmail.com'
        request.session['age'] = 25
        request.session['city'] = 'Perambalur'
        return HttpResponse("Session data set")

    @staticmethod
    def get_session(request):
        username = request.session.get('username', 'Guest')
        email = request.session.get('email', 'Not set')
        age = request.session.get('age', 'Not set')
        city = request.session.get('city', 'Not set')
        return HttpResponse(f"Username: {username}, Email: {email}, Age: {age}, City: {city}")

    @staticmethod
    def set_cookie(request):
        response = HttpResponse("Cookie set")
        response.set_cookie('username', 'Siranjeevis')
        return response

    @staticmethod
    def get_cookie(request):
        username = request.COOKIES.get('username', 'Guest')
        return HttpResponse(f"Username: {username}")


session_cookie_views = SessionCookieViews()








# class Login(View):
#     template_name =  "login.html"
#     success_url = "home"
    
#     def get(self, request, *args: str, **kwargs: Any) :
#         return render(self.request,self.template_name)
#     def post(self,request,*args,**kargs):
#         print(self.request.POST)
#         username = request.COOKIES
        
#         print('username',username)

#         return HttpResponse(username)
    

    # def post(self, request: HttpRequest, *args: str, **kwargs: Any) :
    #         username = request.POST['username']
    #         password = request.POST['password']
    #         print
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             request.session['username'] = username
    #             return redirect(self.success_url)
    #         return super().post(request, *args, **kwargs)

    # Password validation regex
            # password_regex = re.compile(
            #     r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,14}$'
            # )