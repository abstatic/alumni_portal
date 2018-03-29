from .forms import AlumniRegistrationForm, PostForm, JobForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from .models import Alumni, Courses, Branches

# Create your views here.
@login_required
def index(request):
    """
    Logged In -> Redirect to the dashboard page
    Not Logged In -> Render the login page
    """
    return render(request, 'alumni/index.html', {'title': 'Dashboard'})

# add the logged in decorator
def dashboard_view(request):
    """
    Show the dashboard
    """
    return HttpResponse("DASHBOARD VIEW")

def register(request):
    """
    If request type is POST -> Process the form
    If request type is GET -> render the registration page
    """
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        error = ""

        if form.is_valid():
            alumniData = form.cleaned_data

            first_name     = alumniData['first_name']
            last_name      = alumniData['last_name']
            roll_num       = alumniData['roll_num']
            passing_year   = alumniData['passing_year']
            contact_number = alumniData['contact_number']
            branch         = Branches.objects.get(branch_name=alumniData['branch'])
            course         = Courses.objects.get(course_name=alumniData['course'])

            user_name      = alumniData['user_name']
            password       = alumniData['password']
            confirm_pass   = alumniData['confirm_password']
            email          = alumniData['email']

            if password != confirm_pass:
                error = "Passwords don't match"
                return render(request, 'alumni/register.html', {
                    'form': form, 
                    'title': 'Register', 
                    'error': error
                })

            if not (User.objects.filter(username=user_name).exists() or
                User.objects.filter(email=email).exists()):
                
                User.objects.create_user(user_name, email, password)

                a_user = authenticate(username=user_name, passwordd=password)

                user = User.objects.get(email=email)


                al = Alumni.objects.create(
                    user           = user,
                    roll_num       = roll_num,
                    branch         = branch,
                    course         = course,
                    passing_year   = passing_year,
                    contact_number = contact_number
                )

                return HttpResponseRedirect('/')
            else:
                error = "Username or email already exists"
                return render(request, 'alumni/register.html', {
                    'form': form, 
                    'title': 'Register', 
                    'error': error
                })
    else:
        form = AlumniRegistrationForm()
        return render(request, 'alumni/register.html', {'form': form, 'title': 'Register'})

# add the logged in decorator
def search(request):
    """
    search with the given filters in the request
    """
    return HttpResponse("SEARCH VIEW")

def jobs(request):
    """
    render the jobs page
    depending on the page num, show relevant jobs
    Use Cache for fetching
    """
    return HttpResponse("JOBS VIEW")

def posts(request):
    """
    render/return ? the latest posts
    Take in to account the user blocking preferences
    """
    return HttpResponse("POSTS VIEW")

def block_user(request):
    """
    add the user to block list
    """
    return HttpResponse("BLOCK USER VIEW")

def handle_post(request):
    """
    one end point to add/edit/delete blog post

    can have separate function calls to
    """
    return HttpResponse("HANDLE POST VIEW")

def report_offensive(request):
    """
    mark a post as offensive, notify to admin user
    """
    return HttpResponse("REPORT VIEW")

def give_feedback(request):
    """
    send the feedback message to admin user

    GET -> render the feddback page
    POST -> Handle the feedback
    """
    return HttpResponse("GIVE FEEDBACK VIEW")

def subscribe_post(request):
    """
    subscribe to an event/post
    """
    return HttpResponse("SUBS POST VIEW")

def unsubscribe_post(request):
    """
    unsubscribe from an event/post
    """
    return HttpResponse("UNSUBS POST VIEW")

def add_job(request):
    """
    get -> render the job form
    post -> handle the job form
    """
    pass

def events(request):
    """
    """
    return HttpResponse("EVENTS VIEW")