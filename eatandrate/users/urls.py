from django.conf.urls import url, include
from django.contrib.auth import logout
from django.contrib.auth.views import login

from users.forms import MyAuthenticationForm
from . import views
from eatandrate.settings import LOGOUT_REDIRECT_URL


urlpatterns = [
    url(r'^(?P<pk>[\d]+)/$', views.user_profile, name='user_profile'),
    url(r'^myprofile/$', views.my_profile, name='my_profile'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^login/$', login, {'template_name': 'registration\login.html',
                             'authentication_form': MyAuthenticationForm}, name="login"),
    url(r'^logout/$', logout, {'next_page': LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^registerowner/$', views.register_owner, name='register_owner'),
    url(r'^modify_profile/$', views.modify_profile, name='modify_profile'),
    url(r'^delete_profile/$', views.delete_profile, name='delete_profile'),
]
