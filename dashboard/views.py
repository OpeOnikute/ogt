import operator
from django.shortcuts import render
from .models import Job, Client, DesignProblems, PotentialClient, PotentialProject, Inspiration
from .forms import DesignProblemsForm, PotentialClientForm, PotentialProjectForm, InspirationForm, JobForm, ClientForm


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
            already_existing_instance, created = real_model.objects.get_or_create(project_name=data['project_name'])
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

    if modal_type in ['DesignProblemsForm', 'PotentialClientForm', 'PotentialProjectForm', 'InspirationForm', 'ClientForm']:

        modal_model = eval(modal_type)
        real_model = eval(modal_type.strip('Form'))

        already_existing_instance, created = real_model.objects.get_or_create(name=data['name'])

        form_object = modal_model(data, files, instance=already_existing_instance)

        if form_object.is_valid():
            print 'valid!'
            save_it = form_object.save(commit=False)
            save_it.save()
        else:
            print 'Form invalid!'
            print form_object.errors


def index(request):
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
        response = save_modal_data(request.POST, request.FILES)
    context = {
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
    return render(request, 'dashboard/dashboard.html', context)


def projects(request):

    all_projects = Job.objects.all()
    clients = Client.objects.all()
    context = {
        'projects': all_projects,
        'clients': clients,
    }

    if request.method == 'POST':
        response=save_new_job(request.POST, request.FILES)

    return render(request, 'dashboard/projects.html', context)


def clients(request):

    clients = Client.objects.all()
    context = {
        'clients': clients,
    }

    if request.method == 'POST':
        response = save_modal_data(request.POST, request.FILES)

    return render(request, 'dashboard/clients.html', context)


def potential_clients(request):

    potential_clients = PotentialClient.objects.all()
    context = {
        'potential_clients': potential_clients,
    }

    if request.method == 'POST':
        save_modal_data(request.POST, request.FILES)

    return render(request, 'dashboard/potential_clients.html', context)