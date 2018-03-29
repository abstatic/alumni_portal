from django import forms
from .models import Branches, Courses

class JobForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label='Job Description'
    )

    company = forms.CharField(
        required=True,
        label='Company Name'
    )

    author = forms.CharField(
        required=True,
        label='Author Name'
    )

    contact = forms.CharField(
        required=True,
        label='Contact Details'
    )

class PostForm(forms.Form):

    author = forms.CharField(
        required=True,
        label='Author Name'
    )

    content = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label='Post'
    )

    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

class FeedBackForm(forms.Form):
    pass

class AlumniRegistrationForm(forms.Form):

    BRANCHES = tuple(Branches.objects.values_list('branch_name', flat=True))
    COURSES = tuple(Courses.objects.values_list('course_name', flat=True))

    b_choices = []
    for i in range(len(BRANCHES)):
        t_tuple = (BRANCHES[i], BRANCHES[i])
        b_choices.append(t_tuple)
    b_choices = tuple(b_choices)

    c_choices = []
    for i in range(len(COURSES)):
        t_tuple = (COURSES[i], COURSES[i])
        c_choices.append(t_tuple)
    c_choices = tuple(c_choices)


    first_name = forms.CharField(
        required = True,
        label = 'First Name',
        max_length = 20
    )

    last_name = forms.CharField(
        required = True,
        label = 'Last Name',
        max_length = 20
    )

    roll_num = forms.IntegerField(
        required = False,
        label = 'Roll Num (Optional)'
    )

    branch = forms.ChoiceField(choices=b_choices, label="Select Branch", widget=forms.Select(), required=True)
    course = forms.ChoiceField(choices=c_choices, label="Select Course", widget=forms.Select(), required=True)
    passing_year = forms.IntegerField(required=True)
    contact_number = forms.CharField(required=True, max_length=12)

    user_name = forms.CharField(label="Username ")
    password = forms.CharField(label="Password ", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())
    email = forms.EmailField(label="Institute Email")




