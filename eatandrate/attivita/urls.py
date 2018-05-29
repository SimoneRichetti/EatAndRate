from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[\d]+)/$', views.AttView.as_view(), name='detail'),
    url(r'^(?P<pk>[\d]+)/recensisci$', views.recensisci, name='recensisci'),
    url(r'^(?P<pk>[\d]+)/modify$', views.modify, name='modify'),
    url(r'^(?P<pk>[\d]+)/add_image$', views.add_image, name='add_image'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(?P<pk>[\d]+)/delete_image$', views.delete_image, name='delete_image')
]
