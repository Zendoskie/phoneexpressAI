"""
URL configuration for phonexpress project.
"""
from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/phones/', views.phones_api, name='phones_api'),
    path('api/order/', views.create_order, name='create_order'),
]

