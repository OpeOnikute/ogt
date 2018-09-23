import json
from actstream import action
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from constants import Status
from .models import Job, Client, DesignProblems, PotentialClient, PotentialProject, Inspiration, Task, SentEmailsLog, EmailDraft
from .libs.utils import ErrorLogHelper
from .libs.emails import EmailHelper


class BaseView(View):
    """
    All the views that the user interacts with directly to view/edit data should inherit this view
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """
        This executes the route. The decorator makes all routes in child views require a login
        :param args:
        :param kwargs:
        :return:
        """
        return super(BaseView, self).dispatch(*args, **kwargs)

    def save_new_job(self, data):
        """
        We are using different modals, so this function determines which modal it is and saves it's parameters.
        :param data:
        :return string:
        """
        modal_type = data["modal-type"]

        if modal_type == 'JobForm':
            modal_model = eval(modal_type)
            real_model = eval(modal_type.strip('Form'))

            try:
                already_existing_instance = real_model.objects.get(project_name=data['project_name'])
            except Exception, e:
                already_existing_instance = real_model()
                ErrorLogHelper.log_error(e, 'save_form_data')

            form_object = modal_model(data, instance=already_existing_instance)

            if form_object.is_valid():

                save_it = form_object.save(commit=False)
                save_it.start_date = data['date']
                save_it.save()

                # TODO: Have a method to record actions
                verb_text = "just added a new " + modal_type.strip('Form')
                action.send(self.request.user, verb=verb_text, target=already_existing_instance)
            else:
                # TODO: Log the error
                print 'Form invalid!'
                print form_object.errors


class LoginView(View):

    context = {}

    def get(self, request):
        return render(request, 'dashboard/login.html', self.context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard:index'))
        else:
            self.context['userNotFound'] = 'Sorry, this user does not exist.'
            return render(request, 'dashboard/login.html', self.context)


class SignupView(View):

    context = {}

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard:index'))

        signup_form = SignUpForm()
        profile_form = UserProfileForm()

        self.context = {
            'form': signup_form,
            'profile_form': profile_form
        }

        return render(request, 'dashboard/signup.html', self.context)

    def post(self, request):

        signup_form = SignUpForm(request.POST)
        # profile_form = UserProfileForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()
            # profile_form.save()
            return HttpResponseRedirect(reverse('dashboard:index'))
        else:
            self.context['form'] = signup_form
            # self.context['profile_form'] = profile_form
            return render(request, 'dashboard/signup.html', self.context)


class LogoutView(BaseView):

    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect(reverse('dashboard:index'))


class AjaxView(View):
    """
    All views that respond to Ajax calls here
    """

    response = {}

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        This executes the route. The decorator makes all routes in child views exempted from csrf verification
        :param args:
        :param kwargs:
        :return:
        """
        return super(AjaxView, self).dispatch(*args, **kwargs)

    @staticmethod
    def return_ajax_response(server_response):

        return HttpResponse(json.dumps(server_response), content_type="application/json")

    def validate_param(self, param):
        """
        Validates that a parameter being modified belongs to the user
        :param param:
        :return:
        """

        if param.user != self.request.user:
            self.response['status'] = "error"
            self.response['message'] = "You tried to modify a task that belongs to another user. Dont do that."
            return self.return_ajax_response(self.response)

        return True

    def save_form_data(self, data, files):
        """
        We are using different modals, so this function determines which modal it is and saves it's parameters.
        :param data:
        :param files:
        :return string:
        """
        form_type = data["modal-type"]

        if form_type in ['DesignProblemsForm', 'PotentialClientForm', 'PotentialProjectForm', 'InspirationForm',
                         'ClientForm', 'TaskForm', 'ItemPriceForm', 'JobForm']:

            form_model = eval(form_type)
            real_model = eval(form_type.strip('Form'))

            try:
                already_existing_instance = real_model.objects.get(name=data['name'])
            except Exception, e:
                already_existing_instance = real_model()
                ErrorLogHelper.log_error(e, 'save_form_data')

            form_object = form_model(data, files, instance=already_existing_instance)

            if form_object.is_valid():
                print 'valid!'
                save_it = form_object.save(commit=False)
                save_it.save()
                verb_text = "just added a new " + form_type.strip('Form')
                action.send(self.request.user, verb=verb_text, target=already_existing_instance)
            else:
                print 'Form invalid!'
                print form_object.errors


class AjaxSaveFormData(AjaxView):

    def post(self, request):
        data = request.POST
        files = request.FILES

        form_type = data["modal-type"]

        if form_type in ['DesignProblemsForm', 'PotentialClientForm', 'PotentialProjectForm', 'InspirationForm',
                             'ClientForm', 'TaskForm', 'ItemPriceForm', 'JobForm']:

            form_model = eval(form_type)
            real_model = eval(form_type.strip('Form'))

            try:
                already_existing_instance = real_model.objects.get(name=data['name'])
            except Exception, e:
                already_existing_instance = real_model()
                ErrorLogHelper.log_error(e, 'save_form_data')

            form_object = form_model(data, files, instance=already_existing_instance)

            if form_object.is_valid():
                form_target_name = form_type.strip('Form')
                save_it = form_object.save(commit=False)
                save_it.save()
                verb_text = "just added a new " + form_target_name
                action.send(request.user, verb=verb_text, target=already_existing_instance)

                self.response['status'] = "success"
                self.response['message'] = form_target_name + " saved successfully."

                return self.return_ajax_response(self.response)

            else:
                self.response['status'] = "error"
                self.response['message'] = form_object.errors

                return self.return_ajax_response(self.response)

        else:
            self.response['status'] = "error"
            self.response['message'] = "Invalid form type entered."

            return self.return_ajax_response(self.response)


class AjaxSendMessage(AjaxView):
    """
    Sends the email on behalf of the user
    """

    def post(self, request):
        client_id = request.POST['client_id']
        subject = request.POST['subject']
        body = request.POST['body']
        attachments = request.FILES

        client = Client.get_client_by_id(request.user, client_id)

        if client:
            email_helper = EmailHelper()

            email_sent = email_helper.send_email_with_attachments(request, client, subject, body, attachments)

            if email_sent:
                self.response["status"] = "success"

                return self.return_ajax_response(self.response)
            else:
                self.response['message'] = "Technical issue: Email not sent for some reason."

                return self.return_ajax_response(self.response)

        self.response["message"] = "Technical issue: Client not found for some reason."

        return self.return_ajax_response(self.response)


class AjaxGetClient(AjaxView):

    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            client_number = None

            if client.phone_number:
                client_number = int(client.phone_number)

            data = {
                "name": client.name,
                "phone_number": client_number,
                "email": client.email
            }

            self.response["status"] = "success"
            self.response["data"] = data

            return self.return_ajax_response(self.response)

        except Exception, e:
            ErrorLogHelper.log_error(e, 'get_client')

            self.response["message"] = str(e)

            return self.return_ajax_response(self.response)


class IndexView(BaseView):

    context = {}

    def get(self, request):

        all_jobs = Job.objects.filter(user=request.user)
        no_of_clients = Client.get_user_clients(user=request.user, length=True)
        top_clients = Client.get_top_clients(request.user)

        amount_made = Job.get_total_amount_made_by_user(request.user)

        total_completed_jobs = len(all_jobs.filter(completion_status='Yes'))
        total_uncompleted_jobs = len(all_jobs.filter(completion_status='No'))

        design_problems = DesignProblems.objects.filter(user=request.user)

        potential_clients = PotentialClient.objects.filter(user=request.user)
        potential_projects = PotentialProject.objects.filter(user=request.user)

        inspirations = Inspiration.objects.filter(user=request.user)

        self.context = {
            'user': request.user,
            'request': request,
            'amount_made': amount_made,
            'total_completed_jobs': total_completed_jobs,
            'total_uncompleted_jobs': total_uncompleted_jobs,
            'no_of_clients': no_of_clients,
            'design_problems': design_problems,
            'potential_clients': potential_clients,
            'potential_projects': potential_projects,
            'inspirations': inspirations,
            'top_clients': top_clients,
        }

        return render(request, 'dashboard/dashboard.html', self.context)

    def post(self, request):
        AjaxSaveFormData.post(request.POST, request.FILES)
        return self.get(request)


class ProjectsView(BaseView):

    context = {}

    def get(self, request):

        all_projects = Job.objects.filter(user=request.user)
        clients = Client.objects.filter(user=request.user)
        tasks = Task.objects.filter(user=request.user, archived="no")
        tasks_completed = tasks.filter(status=Status.completed)
        tasks_pending = tasks.filter(status=Status.pending)

        self.context = {
            'tasks': tasks,
            'tasks_completed': tasks_completed,
            'tasks_pending': tasks_pending,
            'tasks_archived': Task.objects.filter(user=request.user, archived="yes"),
            'user': request.user,
            'request': request,
            'projects': all_projects,
            'clients': clients,
        }

        project_agg = Task.get_all_projects_and_their_tasks(request.user)

        if project_agg['status'] == "success":
            self.context['project_aggregation'] = project_agg["data"]

        return render(request, 'dashboard/projects.html', self.context)

    def post(self, request):
        if request.POST['modal-type'] == 'JobForm':
            self.save_new_job(request.POST)
        elif request.POST['modal-type'] == 'TaskForm':
            self.save_form_data(request.POST, request.FILES)
            # TODO: Return success or error somehow

        return render(request, 'dashboard/projects.html', self.context)


class ClientsView(BaseView):

    context = {}

    def get(self, request):

        clients = Client.objects.filter(user=request.user)

        self.context = {
            'user': request.user,
            'request': request,
            'clients': clients,
        }

        return render(request, 'dashboard/clients.html', self.context)

    def post(self, request):
        self.save_form_data(request.POST, request.FILES)
        return render(request, 'dashboard/clients.html', self.context)


class PotentialClientsView(BaseView):

    context = {}

    def get(self, request):
        potential_clients = PotentialClient.objects.filter(user=request.user)

        self.context = {
            'user': request.user,
            'request': request,
            'potential_clients': potential_clients,
        }

        return render(request, 'dashboard/potential_clients.html', self.context)

    def post(self, request):
        self.save_form_data(request.POST, request.FILES)
        return render(request, 'dashboard/potential_clients.html', self.context)


class ArchivedTasksView(BaseView):

    context = {}

    def get(self, request):

        archived_tasks = Task.objects.filter(user=request.user, archived='yes')

        self.context = {
            'user': request.user,
            'archived_tasks': archived_tasks,
        }

        return render(request, 'dashboard/archived_tasks.html', self.context)


class PricingView(BaseView):

    context = {}

    def get(self, request):
        items = ItemPrice.objects.filter(user=request.user)

        self.context = {
            'user': request.user,
            'request': request,
            'items': items,
        }

        return render(request, 'dashboard/pricing.html', self.context)

    def post(self, request):
        self.save_form_data(request.POST, request.FILES)
        return render(request, 'dashboard/pricing.html', self.context)


class MessagingView(BaseView):

    context = {}

    def get(self, request):

        try:
            sent_messages = SentEmailsLog.get_user_sent_messages(request.user)
            user_clients = Client.get_user_clients(request.user)
            user_drafts = EmailDraft.get_user_drafts(request.user)

            self.context['sent_messages'] = sent_messages
            self.context['user_clients'] = user_clients
            self.context['user_drafts'] = user_drafts
        except Exception, e:
            ErrorLogHelper.log_error(e, 'messaging_view')

        return render(request, 'dashboard/messaging.html', self.context)


class GenerateQuoteView(BaseView):

    context = {}

    def get(self, request, project_id):

        self.context['request'] = request

        try:
            project = Job.objects.get(id=project_id, user=request.user)
            self.context['project'] = project
        except Exception, e:
            ErrorLogHelper.log_error(e, 'generate_quote_view')

        return render(request, 'dashboard/invoice.html', self.context)


class AjaxUpdateView(AjaxView):
    """
    This view handles all the Ajax calls to modify an object
    """

    def put(self, request, param_type, param_id):

        data = QueryDict(request.body)
        new_value = data['value']

        if param_type == "task":
            try:
                task = Task.objects.get(id=param_id)

                task_valid = self.validate_param(task)

                if task_valid:
                    task.status = new_value
                    verb_text = "just updated Task"
                    action.send(request.user, verb=verb_text, target=task)
                    task.save()

                    self.response['status'] = "success"
                    self.response['message'] = None

                    return self.return_ajax_response(self.response)

            except Exception, e:
                self.response['status'] = "error"
                self.response['message'] = "Something went wrong and the task was not updated."
                ErrorLogHelper.log_error(e, 'update_action')

        return self.return_ajax_response(self.response)

    def delete(self, request, param_type, param_id):

        if param_type == "project":
            try:
                project = Job.objects.get(id=param_id)

                project_valid = self.validate_param(project)

                if project_valid:
                    verb_text = "just deleted Project " + project.project_name
                    action.send(request.user, verb=verb_text)
                    Job.delete(project)

                    self.response['status'] = "success"
                    self.response['message'] = None

            except Exception, e:
                ErrorLogHelper.log_error(e, 'delete_action')

                self.response['status'] = "error"
                self.response['message'] = "Something went wrong and the task was not updated."

        elif param_type == "task":
            try:
                task = Task.objects.get(id=param_id)

                task_valid = self.validate_param(task)

                if task_valid:
                    verb_text = "just deleted Task " + task.description
                    action.send(request.user, verb=verb_text)
                    Task.delete(task)

                    self.response['status'] = "success"
                    self.response['message'] = None

            except Exception, e:
                # TODO: Tell the user that the action failed
                ErrorLogHelper.log_error(e, 'delete_action')

                self.response['status'] = "error"
                self.response['message'] = "Something went wrong and the task was not updated."

        return self.return_ajax_response(self.response)


class AjaxArchiveObjectView(AjaxView):

    action_types = ['archive', 'restore']

    def put(self, request, action_type, param_type, param_id):
        if action_type not in self.action_types:

            self.response['status'] = 'error'
            self.response['message'] = 'Technical issue: invalid action type'

            # TODO: Log all the technical issues

            return self.return_ajax_response(self.response)

        if param_type == "task":
            try:
                task = Task.objects.get(id=param_id)

                # Build the verb used in the actstream display
                verb = str(action_type) + "d"
                verb_text = "just " + verb + " Task"

                task_valid = self.validate_param(task)

                if task_valid:
                    task.archived = "yes" if action_type == "archive" else "no"

                    action.send(request.user, verb=verb_text, target=task)
                    task.save()

                    self.response['status'] = 'success'
                    self.response['message'] = None

            except Exception, e:
                self.response['status'] = 'error'
                self.response['message'] = 'Technical issue: Something went wrong. Please try again.'
                ErrorLogHelper.log_error(e, 'archive_action')

        return self.return_ajax_response(self.response)
