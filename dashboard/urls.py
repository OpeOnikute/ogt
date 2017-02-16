from django.conf.urls import url
from . import views

app_name = "dashboard"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^clients/', views.clients, name='clients'),
    url(r'^potential_clients/', views.potential_clients, name='potential_clients'),

]