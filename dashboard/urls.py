from django.conf.urls import url
from . import views

app_name = "dashboard"
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^signup/', views.signup_view, name='signup'),
    url(r'^projects/', views.projects_view, name='projects'),
    url(r'^ajax_save_form/', views.ajax_save_form_data, name='ajax_save_form'),
    url(r'^clients/', views.clients_view, name='clients'),
    url(r'^client/(?P<client_id>[-\w]+)', views.get_client, name='clients'),
    url(r'^pricing/', views.pricing_view, name='pricing'),
    url(r'^messaging/', views.messaging_view, name='messaging'),
    url(r'^quote/(?P<project_id>[-\w]+)', views.generate_quote_view, name='quote'),
    url(r'^potential_clients/', views.potential_clients_view, name='potential_clients'),
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