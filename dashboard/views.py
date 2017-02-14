import operator
from django.shortcuts import render
from .models import Job, Client, DesignProblems, PotentialClient, PotentialProject, Inspiration


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

    print design_problems

    context = {
        'amount_made': amount_made,
        'total_completed_jobs': total_completed_jobs,
        'total_uncompleted_jobs': total_uncompleted_jobs,
        'no_of_clients': no_of_clients,
        'design_problems': design_problems,
        'potential_clients': potential_clients,
        'potential_projects': potential_projects,
        'inspirations': inspirations,
    }
    return render(request, 'dashboard/index.html', context)