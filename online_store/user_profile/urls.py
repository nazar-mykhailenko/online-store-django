from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'user_profile'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html', authentication_form=LoginForm), name='login'),
    path('logout', views.log_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('order/<int:id>/', views.order_details, name='order_details')
]
