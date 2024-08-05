from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name="login"),
    # path('sindex/', views.sindex, name="sindex"),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'), 
    path('feedback/', views.feedback, name='feedback'),
    path('review/', views.submit_feedback, name='submit_feedback'),
    # path('slogin/', views.slogin, name='slogin'),
    path('questions/', views.questions, name='questions'),
    
    path('next_question/<int:faculty_id>/', views.next_question, name='next_question'),
    path('submit_response/<int:faculty_id>/<int:question_id>/', views.submit_response, name='submit_response'),
    path('feedback_complete/<int:faculty_id>/', views.feedback_complete, name='feedback_complete'),


]