from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^auth/login$', views.LoginView.as_view(),
        name='login'),
    url(r'^auth/register$', views.UserRegistrationView.as_view(),
        name='register'),
    url(r'^bucketlists/$', views.BucketlistListView.as_view(), name='bucketlists'),
    url(r'^bucketlists/(?P<id>[0-9]{1,2})$',
        views.BucketlistDetailView.as_view(), name='bucketlist'),
    url(r'^bucketlists/(?P<id>[0-9]{1,2})/items/$',
        views.ItemsView.as_view(), name='items'),
    url(r'^bucketlists/(?P<bucketlist_id>[0-9]{1,2})/items/(?P<id>[0-9]{1,2})$',
        views.ItemsDetailView.as_view(), name='item'),

]
