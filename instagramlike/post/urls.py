from django.conf.urls import url

from post.views import post_list, post_create

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^create/$', post_create, name='post_create'),
]