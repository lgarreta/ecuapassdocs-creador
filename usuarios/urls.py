from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('base/', views.base, name='base'),
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),

    path('listar/', views.user_list, name='listar'),
    path('crear/', views.UserCreate.as_view(), name='crear'),
    path('actualizar/<pk>', views.UserUpdate.as_view(), name='actualizar'),
    path('eliminar/<pk>', views.UserDelete.as_view(), name='eliminar'),
]
