from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# model for user (alumni)
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20, blank=True)

class Branches(models.Model):
    course_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20, blank=True)

class Alumni(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE)

    alumni_id = models.AutoField(primary_key=True)

    roll_num = models.IntegerField(blank=True, unique=True)

    branch = models.ForeignKey(Branches, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True)

    passing_year = models.IntegerField(blank=False)
    contact_number = models.CharField(blank=False, max_length=13)

    join = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(max_length=350, default="")
    pro_pic = models.ImageField(upload_to="photos/profile_pic", verbose_name="DP", null=True)

    blockList = models.ManyToManyField('Alumni', blank=True)

# model for post
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    content = models.TextField()

class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Image')

# model for job
class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default="")
    company = models.CharField(max_length=100, blank=False)
    content = models.TextField()
    contact = models.CharField(max_length=50)
    timestamp= models.DateTimeField(auto_now_add=True)

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
admin.site.register(Images)
admin.site.register(Courses)
admin.site.register(Branches)