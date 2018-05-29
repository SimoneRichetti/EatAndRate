from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[\d]+)/reply$', views.reply, name='reply'),
    url(r'^(?P<pk>[\d]+)/delete_answer$', views.delete_answer, name='delete_answer'),
    url(r'(?P<pk>[\d]+)/delete_notification$', views.delete_notification, name='delete_notification')
]
