import operator
from actstream import action
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import *
from constants import Status
from .models import Job, Client, DesignProblems, PotentialClient, PotentialProject, Inspiration, Task
from .libs.utils import ErrorLogHelper
from .libs.emails import EmailHelper


def login_view(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:index'))

    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard:index'))
        else:
            context['userNotFound'] = 'Sorry, this user does not exist.'
            return render(request, 'dashboard/login.html', context)

    return render(request, 'dashboard/login.html')


def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse('dashboard:index'))


def signup_view(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    signup_form = SignUpForm()
    profile_form = UserProfileForm()

    context = {
        'form': signup_form,
        'profile_form': profile_form
    }

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if signup_form.is_valid() and profile_form.is_valid():
            signup_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('dashboard:index'))
        else:
            context['form'] = signup_form
            context['profile_form'] = profile_form
            return render(request, 'dashboard/signup.html', context)

    return render(request, 'dashboard/signup.html', context)


def get_total_amount_from_client(client):
    clients_jobs = Job.objects.filter(client=client)
    total_amount = float()
    for job in clients_jobs:
        total_amount += float(job.price)
    return total_amount


def get_top_clients(request):
    clients = Client.objects.filter(user=request.user)
    clients_dict = {}

    for client in clients:
        money_from_client = get_total_amount_from_client(client)
        clients_dict[client.name] = money_from_client

    return sorted(clients_dict.items(), key=operator.itemgetter(1), reverse=True)


def save_new_job(request, data):
    """
         We are using different modals, so this function determines which modal it is and saves it's parameters.
        :param data:
        :param files:
        :return string:
    """
    modal_type = data["modal-type"]

    if modal_type == 'JobForm':
        modal_model = eval(modal_type)
        real_model = eval(modal_type.strip('Form'))

        try:
            already_existing_instance = real_model.objects.get(project_name=data['project_name'])
        except:
            already_existing_instance = real_model()

        form_object = modal_model(data, instance=already_existing_instance)
        # print form_object.as_p()

        if form_object.is_valid():
            print 'valid!'
            save_it = form_object.save(commit=False)
            save_it.start_date = data['date']
            save_it.save()
            verb_text = "just added a new " + modal_type.strip('Form')
            action.send(request.user, verb=verb_text, target=already_existing_instance)
        else:
            print 'Form invalid!'
            print form_object.errors


def save_form_data(request, data, files):
    """
        We are using different modals, so this function determines which modal it is and saves it's parameters.
    :param request:
    :param data:
    :param files:
    :return string:
    """
    form_type = data["modal-type"]

    if form_type in ['DesignProblemsForm', 'PotentialClientForm', 'PotentialProjectForm', 'InspirationForm',
                    'ClientForm', 'TaskForm', 'ItemPriceForm']:

        form_model = eval(form_type)
        real_model = eval(form_type.strip('Form'))

        try:
            already_existing_instance = real_model.objects.get(name=data['name'])
        except:
            already_existing_instance = real_model()

        form_object = form_model(data, files, instance=already_existing_instance)

        if form_object.is_valid():
            print 'valid!'
            save_it = form_object.save(commit=False)
            save_it.save()
            verb_text = "just added a new " + form_type.strip('Form')
            action.send(request.user, verb= verb_text, target=already_existing_instance)
        else:
            print 'Form invalid!'
            print form_object.errors


def index_view(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    fulfilled_jobs = Job.objects.filter(payment_status='Paid', user=request.user)
    amount_made = float()
    for job in fulfilled_jobs:
        amount_made += float(job.price)

    total_completed_jobs = len(Job.objects.filter(completion_status='Yes', user=request.user))
    total_uncompleted_jobs = len(Job.objects.filter(completion_status='No', user=request.user))
    no_of_clients = len(Client.objects.filter(user=request.user))
    top_clients = get_top_clients(request)
    design_problems = DesignProblems.objects.filter(user=request.user)
    potential_clients = PotentialClient.objects.filter(user=request.user)
    potential_projects = PotentialProject.objects.filter(user=request.user)
    inspirations = Inspiration.objects.filter(user=request.user)

    if request.method == 'POST':
        save_form_data(request, request.POST, request.FILES)

    context = {
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
        # 'randJob': randJob,
    }
    return render(request, 'dashboard/dashboard.html', context)


def projects_view(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    all_projects = Job.objects.filter(user=request.user)
    clients = Client.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user, archived="no")
    tasks_completed = tasks.filter(user=request.user, status=Status.completed)
    tasks_pending = tasks.filter(user=request.user, status=Status.pending)

    context = {
        'tasks': tasks,
        'tasks_completed': tasks_completed,
        'tasks_pending': tasks_pending,
        'tasks_archived': Task.objects.filter(user=request.user, archived="yes"),
        'user': request.user,
        'request': request,
        'projects': all_projects,
        'clients': clients,
    }

    project_agg = Task.getAllProjectsAndTheirTasks(request.user)

    if project_agg['status'] == "success":
        context['project_aggregation'] = project_agg["data"]
    else:
        context['project_aggregation'] = project_agg["error"]

    if request.method == 'POST':
        if request.POST['modal-type'] == 'JobForm':
            save_new_job(request, request.POST)
        elif request.POST['modal-type'] == 'TaskForm':
            save_form_data(request, request.POST, request.FILES)

    return render(request, 'dashboard/projects.html', context)


def clients_view(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    clients = Client.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'request': request,
        'clients': clients,
    }

    if request.method == 'POST':
        save_form_data(request, request.POST, request.FILES)

    return render(request, 'dashboard/clients.html', context)


def potential_clients_view(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    potential_clients = PotentialClient.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'request': request,
        'potential_clients': potential_clients,
    }

    if request.method == 'POST':
        save_form_data(request, request.POST, request.FILES)

    return render(request, 'dashboard/potential_clients.html', context)


def archived_tasks_view(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    archived_tasks = Task.objects.filter(user=request.user, archived='yes')
    context = {
        'user': request.user,
        'archived_tasks': archived_tasks,
    }

    return render(request, 'dashboard/archived_tasks.html', context)


def pricing_view(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    items = ItemPrice.objects.filter(user=request.user)

    context = {
        'user': request.user,
        'request': request,
        'items': items,
    }

    if request.method == 'POST':
        save_form_data(request, request.POST, request.FILES)

    return render(request, 'dashboard/pricing.html', context)


def messaging_view(request):

    context = {}

    return render(request, 'dashboard/messaging.html', context)


def generate_quote_view(request, project_id=None):

    context = {
        'request': request
    }

    try:
        project = Job.objects.get(id=project_id, user=request.user)
        context['project'] = project
    except Exception, e:
        print e
        pass

    return render(request, 'dashboard/invoice.html', context)


def update_action(request, param_type, param_id, new_value):

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    if param_type == "task":
        try:
            task = Task.objects.get(id=param_id)

            if task.user != request.user:
                return HttpResponseRedirect(reverse('dashboard:projects'))

            task.status = new_value
            verb_text = "just updated Task"
            action.send(request.user, verb=verb_text, target=task)
            task.save()

        except Exception, e:
            print "Task not found. Sorry"

    return HttpResponseRedirect(reverse('dashboard:projects'))


def delete_action(request, param_type, param_id):

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    if param_type == "project":
        try:
            project = Job.objects.get(id=param_id)

            if project.user != request.user:
                return HttpResponseRedirect(reverse('dashboard:projects'))

            verb_text = "just deleted Project " + project.project_name
            action.send(request.user, verb=verb_text)
            Job.delete(project)

        except Exception, e:
            print "Project not found. Sorry"

    elif param_type == "task":
        print "Task!"
        try:
            task = Task.objects.get(id=param_id)

            if task.user != request.user:
                return HttpResponseRedirect(reverse('dashboard:projects'))

            verb_text = "just deleted Task " + task.description
            action.send(request.user, verb=verb_text)
            Task.delete(task)

        except Exception, e:
            print e

    return HttpResponseRedirect(reverse('dashboard:projects'))


def archive_action(request, action_type, param_type, param_id):

    # Check if the user is logged in and the right action was entered
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    if action_type not in ["archive", "restore"]:
        return HttpResponseRedirect(reverse('dashboard:projects'))

    if param_type == "task":
        try:
            task = Task.objects.get(id=param_id)

            # Build the verb used in the actstream display
            verb = str(action_type) + "d"
            verb_text = "just " + verb + " Task"

            # Prevent a user messing with another user's data
            if task.user != request.user:
                return HttpResponseRedirect(reverse('dashboard:projects'))

            task.archived = "yes" if action_type == "archive" else "no"

            action.send(request.user, verb=verb_text, target=task)
            task.save()

        except Exception, e:
            # The most common exception would be that the task wasn't found
            print e

    return HttpResponseRedirect(reverse('dashboard:projects'))

