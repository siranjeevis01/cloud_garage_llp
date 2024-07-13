from django.urls import path
from .views import user_auth_views, session_cookie_views

urlpatterns = [
    path('register/', user_auth_views.register, name='register'),
    path('login/', user_auth_views.login, name='login'),
    path('home/', user_auth_views.home, name='home'),
    path('logout/', user_auth_views.logout, name='logout'),
    path('set-session/', session_cookie_views.set_session, name='set_session'),
    path('get-session/', session_cookie_views.get_session, name='get_session'),
    path('set-cookie/', session_cookie_views.set_cookie, name='set_cookie'),
    path('get-cookie/', session_cookie_views.get_cookie, name='get_cookie'),
]