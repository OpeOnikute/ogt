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
    url(r'^archive/tasks', views.archived_tasks_view, name='archived_tasks'),
    url(r'^actions/update/(?P<param_type>[-\w]+)/(?P<param_id>[-\w]+)/(?P<new_value>[-\w]+)',
        views.update_action,
        name='update_action'
    ),
    url(r'^actions/delete/(?P<param_type>[-\w]+)/(?P<param_id>[-\w]+)',
        views.delete_action,
        name='delete_action'
    ),

    url(r'^actions/(?P<action_type>[-\w]+)/(?P<param_type>[-\w]+)/(?P<param_id>[-\w]+)',
        views.archive_action,
        name='archive_action'
    ),
]