from django import forms
from .models import Branches, Courses, Images, Post, Job, Event, Alumni, Message
import datetime

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = {'title', 'company', 'content', 'contact'}
        labels = {
            "content": "Job Description",
            "title": "Job Title"
        }
    field_order = ['title', 'company', 'content', 'contact']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        labels = {
            "content": "Post"
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}), 
    label='Image',
    required=False
    )
    class Meta:
        model = Images
        fields = ('image',)

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('topic', 'content',)
        labels = {
            "topic": "Issue",
            "content": "Feedback content: ",
        }

class AlumniRegistrationForm(forms.ModelForm ):
    password = forms.CharField(label="Password ", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    class Meta:
        model = Alumni
        exclude = ['user', 'join', 'blockList']
        labels = {
            "email": "Institute Email",
            "roll_num": "Roll Num (Optional)"
        }

class SearchForm(forms.Form):
    BRANCHES = tuple(Branches.objects.values_list('branch_name', flat=True))
    BRANCHES_ID = tuple(Branches.objects.values_list('course_id', flat=True))
    b_choices = []
    for i in range(len(BRANCHES)):
        t_tuple = (BRANCHES_ID[i], BRANCHES[i])
        b_choices.append(t_tuple)
    b_choices.insert(0, ('All', 'All'))
    b_choices = tuple(b_choices)
    branch = forms.ChoiceField(choices=b_choices, label="Select Branch", widget=forms.Select(), required=True)

    COURSES = tuple(Courses.objects.values_list('course_name', flat=True))
    COURSES_ID = tuple(Courses.objects.values_list('course_id', flat=True))
    c_choices = []
    for i in range(len(COURSES)):
        t_tuple = (COURSES_ID[i], COURSES[i])
        c_choices.append(t_tuple)
    c_choices.insert(0, ('All', 'All'))
    c_choices = tuple(c_choices)
    course = forms.ChoiceField(choices=c_choices, label="Select Course", widget=forms.Select(), required=True)

    years = []
    now = datetime.datetime.now()
    year = now.year
    for i in range(1990, year+1):
        t_tuple = (i, i)
        years.append(t_tuple)
    years.insert(0, ('All', 'All'))
    years = tuple(years)
    passing_year = forms.ChoiceField(choices=years)

    first_name = forms.CharField(required=False, initial="All")
    last_name = forms.CharField(required=False, initial="All")
    roll_num = forms.IntegerField(required=False, initial=0)