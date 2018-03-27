from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard_view),
    url(r'^register$', views.register),
    url(r'^search$', views.search),
    url(r'^jobs$', views.jobs),
    url(r'^blockUser$', views.block_user),
    url(r'^handlePost$', views.handle_post),
    url(r'^report$', views.report_offensive),
    url(r'^feedback$', views.give_feedback),
    url(r'^subscribe$', views.subscribe_post),
    url(r'^unsubscribe$', views.unsubscribe_post)
]