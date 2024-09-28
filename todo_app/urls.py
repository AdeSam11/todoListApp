from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login-page'),
    path('logout/', views.logoutView, name='logout'),
    path('delete-task/<int:id>', views.deleteTask, name='delete'),
    path('update-task/<int:id>', views.updateTask, name='update'),
]