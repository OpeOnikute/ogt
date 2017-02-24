import operator
import django.core.exceptions as DjangoExceptions
from actstream import action
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Job, Client, DesignProblems, PotentialClient, PotentialProject, Inspiration, Task
from .forms import *


def loginView(request):

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


def logoutView(request):

    logout(request)
    return HttpResponseRedirect(reverse('dashboard:index'))



def signupView(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    signupForm = SignUpForm()

    context = {
        'form': signupForm,
    }

    if request.method == 'POST':
        signupForm = SignUpForm(request.POST)
        if signupForm.is_valid():
           # ksdbk
            pass
        else:
            context['form'] = signupForm
            return render(request, 'dashboard/login.html', context)

    return render(request, 'dashboard/signup.html', context)


def get_total_amount_from_client(client):
    clients_jobs = Job.objects.filter(client=client)
    total_amount = float()
    for job in clients_jobs:
        total_amount += float(job.price)
    return total_amount


def get_top_clients():
    clients = Client.objects.all()
    clients_dict = {}

    for client in clients:
        money_from_client = get_total_amount_from_client(client)
        clients_dict[client.name] = money_from_client

    return sorted(clients_dict.items(), key=operator.itemgetter(1), reverse=True)


def save_new_job(data, files):
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
            already_existing_instance, created = real_model.objects.get(project_name=data['project_name'])
        except:
            already_existing_instance = real_model()

        form_object = modal_model(data, files, instance=already_existing_instance)
        print form_object.as_p()

        if form_object.is_valid():
            print 'valid!'
            save_it = form_object.save(commit=False)
            save_it.start_date = data['date']
            save_it.save()
        else:
            print 'Form invalid!'
            print form_object.errors


def save_modal_data(data, files):
    """
        We are using different modals, so this function determines which modal it is and saves it's parameters.
    :param data:
    :param files:
    :return string:
    """
    modal_type = data["modal-type"]

    if modal_type in ['DesignProblemsForm', 'PotentialClientForm', 'PotentialProjectForm', 'InspirationForm',
                      'ClientForm', 'TaskForm']:

        modal_model = eval(modal_type)
        real_model = eval(modal_type.strip('Form'))

        try:
            already_existing_instance = real_model.objects.get(name=data['name'])
        except:
            already_existing_instance = real_model()

        form_object = modal_model(data, files, instance=already_existing_instance)

        if form_object.is_valid():
            print 'valid!'
            save_it = form_object.save(commit=False)
            save_it.save()
        else:
            print 'Form invalid!'
            print form_object.errors


def index(request):

    # Make the user log in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    # RandClient = Client.objects.get(id=1)
    randJob = Job.objects.get(id=2)
    # action.send(randJob, verb='is now linked to', target=RandClient)
    fulfilled_jobs = Job.objects.filter(payment_status='Paid')
    amount_made = float()
    for job in fulfilled_jobs:
        amount_made += float(job.price)

    total_completed_jobs = len(Job.objects.filter(completion_status='Yes'))
    total_uncompleted_jobs = len(Job.objects.filter(completion_status='No'))
    no_of_clients = len(Client.objects.all())
    top_clients = get_top_clients()
    design_problems = DesignProblems.objects.all()
    potential_clients = PotentialClient.objects.all()
    potential_projects = PotentialProject.objects.all()
    inspirations = Inspiration.objects.all()

    if request.method == 'POST':
        save_modal_data(request.POST, request.FILES)

    context = {
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
        'randJob': randJob,
    }
    return render(request, 'dashboard/dashboard.html', context)


def projects(request):

    all_projects = Job.objects.all()
    clients = Client.objects.all()
    tasks = Task.objects.all().order_by('date')

    context = {
        'request': request,
        'projects': all_projects,
        'clients': clients,
        'tasks': tasks,
    }

    if request.method == 'POST':
        if request.POST['modal-type'] == 'JobForm':
            save_new_job(request.POST, request.FILES)
        elif request.POST['modal-type'] == 'TaskForm':
            save_modal_data(request.POST, request.FILES)

    return render(request, 'dashboard/projects.html', context)


def clients(request):

    clients = Client.objects.all()
    context = {
        'request': request,
        'clients': clients,
    }

    if request.method == 'POST':
        response = save_modal_data(request.POST, request.FILES)

    return render(request, 'dashboard/clients.html', context)


def potential_clients(request):

    potential_clients = PotentialClient.objects.all()
    context = {
        'request': request,
        'potential_clients': potential_clients,
    }

    if request.method == 'POST':
        save_modal_data(request.POST, request.FILES)

    return render(request, 'dashboard/potential_clients.html', context)


def update_task(request, task_id, status):

    try:
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
    except:
        print "Task not found. Sorry"

    return HttpResponseRedirect(reverse('dashboard:projects'))
