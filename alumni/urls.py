from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^search$', views.search),
    url(r'^jobs$', views.jobs),
    url(r'^addjobs$', views.add_job),
    url(r'^addpost$', views.add_post),
    url(r'^blockUser$', views.block_user),
    url(r'^handlePost$', views.handle_post),
    url(r'^report$', views.report_offensive),
    url(r'^feedback$', views.give_feedback),
    url(r'^subscribe$', views.subscribe_post),
    url(r'^unsubscribe$', views.unsubscribe_post),
    url(r'^login', auth_views.login, {'template_name': 'admin/login.html'}),
    url(r'^logout', auth_views.logout),
    url(r'^events$', views.events)
]