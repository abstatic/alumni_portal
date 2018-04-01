from .forms import AlumniRegistrationForm, PostForm, JobForm, SearchForm, ImageForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from .models import Alumni, Courses, Branches, Images, Post, Job
from django.forms import formset_factory

# Create your views here.
@login_required
def index(request):

    posts = Post.objects.all().order_by('timestamp')[:10]

    import pdb
    pdb.set_trace()

    return render(request, 'alumni/index.html', {
        'title': 'Dashboard',
        'posts': posts
        })

@login_required
def my_jobs(request):
    pass

@login_required
def my_posts(request):
    alum = Alumni.objects.get(user=request.user)
    posts = Post.objects.filter(author=alum)

    return render(request, 'alumni/index.html', {
        'title': "Your posts",
        'posts': posts,
        'my_posts': True
    })

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
                
                User.objects.create_user(
                    user_name, email, password, 
                    first_name=first_name, last_name=last_name)

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

@login_required
def search(request):
    """
    search with the given filters in the request
    """
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            search_data = form.cleaned_data



        return render(request, 'alumni/search.html', {
            'title': 'Search Results',
            'search_form': False
            })
    else:
        form = SearchForm()
        return render(request, 'alumni/search.html', {
            'form': form, 
            'title': 'Search Alumni',
            'search_form': True
            })

@login_required
def add_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, prefix="post")
        img_form = ImageForm(request.POST, request.FILES , prefix="img")

        if post_form.is_valid() and img_form.is_valid():
            post_form_inst = post_form.save(commit=False)
            post_form_inst.author = Alumni.objects.get(user=request.user)
            post_form_inst.save()

            img_form_inst = img_form.save(commit=False)
            img_form_inst.post = post_form_inst
            img_form_inst.save()

            return HttpResponseRedirect("/")
        else:
            error = "Invalid Form Filled"
            form = PostForm(prefix="post")
            img_form = ImageForm(prefix="img")
            return render(request, 'alumni/add_post.html', {
                'form': form, 
                'title': 'Add Post',
                'img_form': img_form,
                'error': error
                })
    else:
        title = 'Add Post'
        pid = None
        if 'pid' in request.GET:
            pid = request.GET['pid']
        
        if pid:
            try:
                post = Post.objects.get(post_id=pid)
                form = PostForm(prefix="post", instance=post)
            except:
                return HttpResponseRedirect('/')
            title = 'Edit Post'
        else:
            form = PostForm(prefix="post")

        img_form = ImageForm(prefix="img")
        return render(request, 'alumni/add_post.html', {
            'form': form, 
            'title': title,
            'img_form': img_form
            })

@login_required
def post(request):
    if 'pid' in request.GET:
        pid = request.GET['pid']
    else:
        return HttpResponseRedirect('/')

    try:
        post = Post.objects.get(post_id=pid)
    except:
        return HttpResponseRedirect('/')

    return render(request, 'alumni/post.html', {
        'post': post,
        'title': 'Post'
    })

@login_required
def profile(request):
    if 'uid' in request.GET:
        u_id = request.GET['uid']
    else:
        return HttpResponseRedirect('/')

    try:
        alumni = Alumni.objects.get(user__id=u_id)
        return render(request, 'alumni/profile.html', {
            'alumni': alumni,
            'title': 'Alumni Profile'
        })
    except:
        return HttpResponseRedirect('/')

def jobs(request):
    """
    render the jobs page
    depending on the page num, show relevant jobs
    Use Cache for fetching
    """
    jobs = Job.objects.all()[:10]
    return render(request, 'alumni/jobs.html', {
        'jobs': jobs
    })

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
    if request.method == "POST":
        job_form = JobForm(request.POST, prefix="job")

        if job_form.is_valid():
            job_form_inst = job_form.save(commit=False)
            job_form_inst.author = Alumni.objects.get(user=request.user)
            job_form_inst.save()

            return HttpResponseRedirect("/jobs")
        else:
            error = "Invalid Form Filled"
            form = JobForm(prefix="job")
            return render(request, 'alumni/add_job.html', {
                'form': form, 
                'title': 'Add Job',
                'error': error
                })
    else:
        form = JobForm(prefix="job")
        return render(request, 'alumni/add_job.html', {
            'form': form, 
            'title': 'Add Job',
            })


def events(request):
    """
    """
    return HttpResponse("EVENTS VIEW")