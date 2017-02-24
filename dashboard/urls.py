from django.conf.urls import url
from . import views

app_name = "dashboard"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.loginView, name='login'),
    url(r'^logout/', views.logoutView, name='logout'),
    url(r'^signup/', views.signupView, name='signup'),
    url(r'^projects/', views.projects, name='projects'),
    url(r'^clients/', views.clients, name='clients'),
    url(r'^potential_clients/', views.potential_clients, name='potential_clients'),
    url(r'^update_task/(?P<task_id>[-\w]+)/(?P<status>[-\w]+)', views.update_task, name='update_task'),

]