from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# model for user (alumni)
class Alumni(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE)

    # Choices for Branches
    BRANCHES = (
        ('CSE', 'Computer Science Engineering'),
        ('CSD', 'CSD')
    )

    # Choices for Courses    
    # First value is value stored in DB
    COURSES = (
        ('PhD', 'PhD'),
        ('BTech', 'BTech'),
        ('MTech', 'MTech')
    )

    alumni_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, blank=False)

    roll_num = models.IntegerField(blank=True, unique=True)

    branch = models.CharField(max_length=5, blank=False, choices=BRANCHES)
    course = models.CharField(max_length=5, blank=False, choices=COURSES)

    passing_year = models.IntegerField(blank=False)
    contact_number = models.IntegerField(blank=False)

# model for photos
class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=100, blank=False)

# model for post
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    content = models.TextField()
    photos = models.ManyToManyField(Photo)

# model for job
class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, blank=False)
    contact = models.CharField(max_length=50)
    content = models.CharField(max_length=300)

# model for event
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    duration = models.CharField(max_length=20)
    content = models.CharField(max_length=400)

# model for message
class Message(models.Model):
    msg_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=300)

admin.site.register(Message)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(Job)
admin.site.register(Alumni)
admin.site.register(Photo)
