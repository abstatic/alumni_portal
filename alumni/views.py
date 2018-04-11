from .forms import AlumniRegistrationForm, PostForm, JobForm, SearchForm, ImageForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from .models import Alumni, Courses, Branches, Images, Post, Job, Event
from django.forms import formset_factory
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required
def index(request):

    posts = Post.objects.all().order_by('timestamp')

    filtered_posts = []

    current_alum = get_object_or_404(Alumni, user__id=request.user.id)

    for post in posts:
        if post.author.user.id not in current_alum.blockList:
            filtered_posts.append(post)
    
    return render(request, 'alumni/index.html', {
        'title': 'Dashboard',
        'posts': filtered_posts
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
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            alumniData = form.cleaned_data

            user_name      = alumniData['user_name']
            password       = alumniData['password']
            confirm_pass   = alumniData['confirm_password']
            email          = alumniData['email']

            dp             = request.FILES['pro_pic']

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

                user = User.objects.get(email=email)

                al = form.save(commit=False)
                al.user = user
                al.save()

                return HttpResponseRedirect('/')
            else:
                uid = None
                if 'uid' in request.POST and request.POST['uid'] == request.user.id:
                    import pdb
                    pdb.set_trace()
                    uid = request.POST['uid']
                    user = User.objects.get(id=uid)
                    passwordForm = PasswordChangeForm(request.user, request.POST)

                    if passwordForm.is_valid():
                        user = passwordForm.save()
                        update_session_auth_hash(request, user)
                    
                    return HttpResponseRedirect("/")
                else:
                    error = "Username or email already exists"
                    return render(request, 'alumni/register.html', {
                        'form': form, 
                        'title': 'Register', 
                        'error': error
                    })
        else:
            error = form.errors
            return render(request, 'alumni/register.html', {
                'form': form, 
                'title': 'Register', 
                'error': error
            })

    else:
        title = 'Create Profile'
        uid = None
        if 'uid' in request.GET:
            uid = int(request.GET['uid'])
            if uid != request.user.id:
                uid = None

        if uid:
            alumni = Alumni.objects.get(user=request.user)
            form = AlumniRegistrationForm(instance=alumni)
            title = 'Edit Profile'
        else:
            form = AlumniRegistrationForm()

        return render(request, 'alumni/register.html', {
            'form': form, 
            'title': title,
            'uid': uid
        })

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

        pid = None
        if 'pid' in request.POST:
            pid = request.POST['pid']

            try:
                post = Post.objects.get(post_id=pid)
                post.images_set.all().delete()
            except:
                return HttpResponseRedirect("/")

        if post_form.is_valid():

            if pid is not None:
                post_form = PostForm(request.POST, instance=post, prefix="post")
                if post_form.is_valid():
                    post_form.save()
                post_form_inst = post
            else:
                post_form_inst = post_form.save(commit=False)
                post_form_inst.author = Alumni.objects.get(user=request.user)
                post_form_inst.save()

            if len(request.FILES) > 0:
                files = request.FILES.getlist('img-image')

                for f in files:
                    current_image = Images(
                        post = post_form_inst,
                        image = f
                    )
                    current_image.save()

            return HttpResponseRedirect("/")
        else:
            error = "Invalid Form Filled"
            form = PostForm(prefix="post")
            img_form = [ImageForm(prefix="img")]
            return render(request, 'alumni/add_post.html', {
                'form': form, 
                'title': 'Add Post',
                'img_forms': img_form,
                'error': error
                })
    else:
        title = 'Add Post'
        pid = None
        if 'pid' in request.GET:
            pid = request.GET['pid']
        
        img_forms = []

        # executed in case of EDIT
        if pid:
            try:
                post = Post.objects.get(post_id=pid)
                images = post.images_set.all()
                form = PostForm(prefix="post", instance=post)
                for img in images:
                    img_form = ImageForm(prefix="img", instance=img)
                    img_forms.append(img_form)
                img_forms.append(ImageForm(prefix="img"))
            except:
                return HttpResponseRedirect('/')
            title = 'Edit Post'
        else:
            form = PostForm(prefix="post")
            img_forms.append(ImageForm(prefix="img"))

        return render(request, 'alumni/add_post.html', {
            'form': form, 
            'title': title,
            'img_forms': img_forms,
            'pid': pid
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

@login_required
def block_user(request):
    """
    add the user to block list
    """
    if 'uid' in request.GET:
        blocked_uid = request.GET['uid']
        try:
            blocked_user = User.objects.get(id=blocked_uid)
        except:
            return HttpResponseRedirect("/")

    current_alumni = get_object_or_404(Alumni, user__id=request.user.id)

    if blocked_uid not in current_alumni.blockList:
        current_alumni.blockList.append(blocked_uid)
        current_alumni.save()

    return HttpResponseRedirect("/")

def delete(request):
    if 'pid' in request.GET:
        post = get_object_or_404(Post, post_id=request.GET['pid'])

        post_author = post.author
        current_alum = Alumni.objects.get(user=request.user)

        if post_author == current_alum:
            post.delete()
        return HttpResponseRedirect("/myposts")

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
    if 'eid' in request.GET:
        event = get_object_or_404(Event, event_id=request.GET['eid'])

        uid = request.user.id
        if uid not in event.subscribed:
            event.subscribed.append(uid)
        event.save()
        return HttpResponseRedirect('/events')

def unsubscribe_post(request):
    """
    unsubscribe from an event/post
    """
    if 'eid' in request.GET:
        event = get_object_or_404(Event, event_id=request.GET['eid'])

        uid = request.user.id

        if uid in event.subscribed:
            event.subscribed.remove(uid)
        event.save()
        return HttpResponseRedirect('/events')

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


@login_required
def events(request):
    events = Event.objects.all()

    return render(request, 'alumni/events.html', {
        'events': events,
        'title': 'Alumni Events'
    })

@login_required
def my_events(request):
    curr_uid = request.user.id
    events = Event.objects.filter(subscribed__contains=[curr_uid])

    return render(request, 'alumni/events.html', {
        'events': events,
        'title': 'Your Events'
    })

@login_required
def block_list(request):
    """
    """
    current_alum = get_object_or_404(Alumni, user__id=request.user.id)

    blocked_users = current_alum.blockList

    blocked = Alumni.objects.filter(user__id__in=blocked_users)

    

@login_required
def unblock(request):
    return HttpResponseRedirect("/")