from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_slot, name='book_slot'),
    path('business/', views.business, name='business'),
    path('contact/', views.contact, name='contact'),
]
