from django.conf.urls import url
from . import views          
  
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_page$', views.login_page),
    url(r'^login$', views.login),
    url(r'^travel$', views.travel),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),        
]