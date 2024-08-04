from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .feedback_analyzer import generate_faculty_review

# Create your views here.
def questions(request):
    faculties = Faculty.objects.all()
    questions = Question.objects.all()
    return render(request, 'questions.html')

def index(request):
    if request.user.is_authenticated:
        faculties = Faculty.objects.all()
        return render(request, 'index.html', {'user': request.user, 'faculties': faculties})
    else:
        return render(request, 'index.html')
    
def sindex(request):
    faculties = Faculty.objects.all()
    return render(request, 'sindex.html', {'faculties': faculties})

def next_question(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    answered_questions = Opinions.objects.filter(user=request.user, faculty=faculty).values_list('question', flat=True)
    next_question = Question.objects.exclude(id__in=answered_questions).first()
    if not next_question:
        # If all questions are answered, redirect to a completion page or next faculty
        return redirect('feedback_complete', faculty_id=faculty.id)
    return render(request, 'questions.html', {'faculty': faculty, 'question': next_question})

def submit_response(request, faculty_id, question_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        faculty = get_object_or_404(Faculty, id=faculty_id)
        question = get_object_or_404(Question, id=question_id)
        opinion, created = Opinions.objects.get_or_create(user=request.user, faculty=faculty, question=question, defaults={'value': rating})
        if not created:
            opinion.value = rating
            opinion.save()
        return redirect('next_question', faculty_id=faculty.id)
    
def feedback_complete(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    return render(request, 'success_message.html', {'faculty': faculty})

def feedback_page(request):
    questions = Question.objects.all()
    return render(request, 'feedback_form.html', {'questions': questions})

def submit_feedback(request):
    if request.method == 'POST':
        faculty_id = request.POST['faculty']
        faculty = get_object_or_404(Faculty, id=faculty_id)
        opinions = []
        for question in Question.objects.all():
            value = int(request.POST.get(f'question_{question.id}'))
            opinion, created = Opinions.objects.get_or_create(
                user=request.user,
                faculty=faculty,
                question=question,
                defaults={'value': value}
            )
            if not created:
                opinion.value = value
                opinion.save()
            opinions.append(opinion)
        review = generate_faculty_review(Question.objects.all(), opinions)
        Review.objects.create(user=request.user, faculty=faculty, review_text=review)

        return render(request, 'review_page.html', {'review': review})
    else:
        return redirect('index')
    
def feedback(request):
    if request.method == 'POST':
        faculty_id = request.POST['faculty']
        faculty = get_object_or_404(Faculty, id=faculty_id)
        questions = Question.objects.all()
        return render(request, 'feedback_form.html', {'faculty': faculty, 'questions': questions})
    else:
        return redirect('index')
 

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=password)
                return redirect('login')  # Redirect to the login page after successful registration
            else:
                error_message = "Email already exists."
        else:
            error_message = "Passwords do not match."
        return render(request, 'registration_form.html', {'error_message': error_message})
    else:
        return render(request, 'registration_form.html')
    
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the home page or any other page after login
        else:
            error_message = "Invalid email or password."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('index') 
    
   







