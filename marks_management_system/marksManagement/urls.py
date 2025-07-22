from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginAsFaculty, name='loginAsFaculty'), 
    path('login/', views.loginAsFaculty, name='loginAsFaculty'),
    path('logout/', views.faculty_logout, name='faculty_logout'),
    path('dashboard/', views.facultydashboard, name='facultydashboard'),
    path('manage-student-entry/', views.manage_student_entry, name='manage_student_entry'), 
    path('manage-student-entry/<int:pk>/', views.manage_student_entry, name='manage_student_entry'), 
    path('delete-student-entry/<int:pk>/', views.delete_student_entry, name='delete_student_entry'),
]