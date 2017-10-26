from django.conf.urls import url

from member.views import signup

urlpatterns = [
    url(r'^signup/$', signup, name="signup" )
]