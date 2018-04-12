from .forms import AlumniRegistrationForm, PostForm, JobForm, SearchForm, ImageForm, FeedBackForm
from .models import Alumni, Courses, Branches, Images, Post, Job, Event, Report
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
import django_comments

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
    if request.method == "POST":
        form = SearchForm(request.POST)

        qset = Alumni.objects.all()
        if form.is_valid():
            search_data = form.cleaned_data

            branch = search_data['branch']
            course = search_data['course']
            passing_year = search_data['passing_year']
            first_name = search_data['first_name']
            last_name = search_data['last_name']
            roll_num = search_data['roll_num']
            
            if branch != 'All':
                qset = qset.filter(branch=branch)

            if course != 'All':
                qset = qset.filter(course=course)

            if passing_year != 'All':
                qset = qset.filter(passing_year=passing_year)

            if first_name != 'All':
                qset = qset.filter(first_name__icontains=first_name)

            if last_name != 'All':
                qset = qset.filter(last_name__icontains=last_name)

            if roll_num != 0:
                qset = qset.filter(roll_num=roll_num)

        return render(request, 'alumni/search.html', {
            'title': 'Search Results',
            'search_form': False,
            'search_res': qset
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

@login_required
def jobs(request):
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

@login_required
def report_offensive(request):
    """
    mark a post as offensive, notify to admin user
    """
    reported_by = get_object_or_404(Alumni, user__id=request.user.id)

    if 'pid' in request.GET:
        try:
            pid = int(request.GET['pid'])
            post = get_object_or_404(Post, post_id=pid)
        except:
            return HttpResponseRedirect("/")

    report = Report.objects.get_or_create(reported_by=reported_by, post=post)[0]
    report.save()

    return HttpResponseRedirect("/")

@login_required
def my_jobs(self):
    return HttpResponse("JOBS EDIT")

@login_required
def give_feedback(request):

    if request.method == "GET":

        form = FeedBackForm()

        return render(request, 'alumni/feedback.html', {
            'form': form,
            'title': "Feedback"
        })
    else:
        feedbackform = FeedBackForm(request.POST)

        if feedbackform.is_valid():
            feedbackform_inst = feedbackform.save(commit=False)
            feedbackform_inst.message_by = Alumni.objects.get(user=request.user)
            feedbackform_inst.save()

        return HttpResponseRedirect("/")
        
@login_required
def subscribe_post(request):
    if 'eid' in request.GET:
        event = get_object_or_404(Event, event_id=request.GET['eid'])

        uid = request.user.id
        if uid not in event.subscribed:
            event.subscribed.append(uid)
        event.save()
        return HttpResponseRedirect('/events')

@login_required
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

@login_required
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
    current_alum = get_object_or_404(Alumni, user__id=request.user.id)

    blocked_users = current_alum.blockList

    blocked = Alumni.objects.filter(user__id__in=blocked_users)

    return render(request, 'alumni/blocklist.html', {
        'blocklist': blocked,
        'title': "Blocked Users"
    })

@login_required
def unblock(request):
    current_alumni = get_object_or_404(Alumni, user__id=request.user.id)
    if 'uid' in request.GET:
        try:
            blocked_uid = int(request.GET['uid'])
            blocked_user = User.objects.get(id=blocked_uid)
        except:
            if blocked_uid in current_alumni.blockList:
                current_alumni.blockList.remove(blocked_uid)
                current_alumni.save()
            return HttpResponseRedirect("/myblocked")


    if blocked_uid in current_alumni.blockList:
        current_alumni.blockList.remove(blocked_uid)
        current_alumni.save()

    return HttpResponseRedirect("/myblocked")

@login_required
def delete_own_comment(request):
    message_id = request.GET['cid']
    comment = get_object_or_404(django_comments.get_model(), pk=message_id,
            site__pk=settings.SITE_ID)
    if comment.user == request.user:
        comment.is_removed = True
        comment.save()

    return redirect(request.META['HTTP_REFERER'])
    