from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    Logged In -> Redirect to the dashboard page
    Not Logged In -> Render the login page
    """
    return render(request, 'alumni/index.html', {'q': 1})

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
    return HttpResponse("REGISTER VIEW")

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