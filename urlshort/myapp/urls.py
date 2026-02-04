from django.urls import path
from . import views

urlpatterns=[
    path('register/', views.register, name='register'),
    path('login/', views.Loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('', views.home, name='home'),
    path('shorten_url/', views.CreateshortLink, name='shorten_url'),
    path('<str:pk>', views.shortlink, name='shortlink'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_link/<int:pk>/', views.delete_link, name='delete_link'),
    path('edit_link/<int:pk>/', views.edit_link, name='edit_link'),

]

