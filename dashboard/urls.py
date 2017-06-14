from django.conf.urls import url
from . import views

app_name = "dashboard"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login', views.LoginView.as_view(), name='login'),
    url(r'^logout', views.LogoutView.as_view(), name='logout'),
    url(r'^signup', views.SignupView.as_view(), name='signup'),
    url(r'^projects', views.ProjectsView.as_view(), name='projects'),
    url(r'^ajax/form', views.AjaxSaveFormData.as_view(), name='ajax_save'),
    url(r'^ajax/send_message', views.AjaxSendMessage.as_view(), name='ajax_send_message'),
    url(r'^ajax/client/(?P<client_id>[-\w]+)', views.AjaxGetClient.as_view(), name='get_client'),
    url(r'^clients', views.ClientsView.as_view(), name='clients'),
    url(r'^pricing', views.PricingView.as_view(), name='pricing'),
    url(r'^messaging', views.MessagingView.as_view(), name='messaging'),
    url(r'^quote/(?P<project_id>[-\w]+)', views.GenerateQuoteView.as_view(), name='quote'),
    url(r'^potential_clients', views.PotentialClientsView.as_view(), name='potential_clients'),
    url(r'^archive/tasks', views.ArchivedTasksView.as_view(), name='archived_tasks'),
    url(r'^actions/(?P<param_type>[-\w]+)/(?P<param_id>[-\w]+)',
        views.AjaxUpdateView.as_view(),
        name='update_action'),
    url(r'^actions/(?P<action_type>[-\w]+)/(?P<param_type>[-\w]+)/(?P<param_id>[-\w]+)',
        views.AjaxArchiveObjectView.as_view(),
        name='archive_action'),
    ]
