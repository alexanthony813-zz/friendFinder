from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/', views.search_dogs),
    url(r'^login/', views.login),
    url(r'^logout/', views.user_logout),
]
