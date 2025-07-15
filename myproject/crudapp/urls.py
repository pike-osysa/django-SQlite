from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),  # ✅ Add this
    path('register/',views.register,name='register'),
    path('logout/', views.log_out, name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]
    
    


    

