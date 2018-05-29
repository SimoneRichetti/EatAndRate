from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)/vote_pos$', views.vote_pos, name='vote_pos'),
    url(r'^(?P<pk>[\d]+)/vote_neg$', views.vote_neg, name='vote_neg'),
]
