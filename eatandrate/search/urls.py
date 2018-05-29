from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^simple_search/', views.simple_search, name='simple_search'),
    url(r'^(?P<pk>[\d]+)/simple_results/$', views.simple_results, name='simple_results'),
    url(r'^complex_search/', views.complex_search, name='complex_search'),
    url(r'^(?P<pk>[\d]+)/complex_results/$', views.complex_results, name='complex_results'),
]
