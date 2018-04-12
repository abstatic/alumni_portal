from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^addjob$', views.add_job),
    url(r'^addpost$', views.add_post),
    url(r'^block$', views.block_user),
    url(r'^blockUser$', views.block_user),
    url(r'^deletepost$', views.delete),
    url(r'^editpost$', views.add_post),
    url(r'^editprofile$', views.register),
    url(r'^events$', views.events),
    url(r'^feedback$', views.give_feedback),
    url(r'^jobs$', views.jobs),
    url(r'^login', auth_views.login, {'template_name': 'alumni/login.html'}),
    url(r'^logout', auth_views.logout),
    url(r'^myblocked$', views.block_list),
    url(r'^myevents$', views.my_events),
    url(r'^myjobs$', views.my_jobs),
    url(r'^myposts', views.my_posts),
    url(r'^post$', views.post),
    url(r'^register$', views.register),
    url(r'^report$', views.report_offensive),
    url(r'^search$', views.search),
    url(r'^subscribe$', views.subscribe_post),
    url(r'^unblock$', views.unblock),
    url(r'^unsubscribe$', views.unsubscribe_post),
    url(r'^users$', views.profile),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^deletecomment$', views.delete_own_comment)
]