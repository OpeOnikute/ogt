from django import forms
from .models import Job, DesignProblems, PotentialClient, PotentialProject, Inspiration, Client


class DesignProblemsForm(forms.ModelForm):

    class Meta:
        model = DesignProblems
        fields = ('name', 'description', 'potential_solution', 'profit_opportunities')


class PotentialClientForm(forms.ModelForm):

    class Meta:
        model = PotentialClient
        fields = ('name', 'reason', 'how_to_get_client', 'best_way_to_contact')


class PotentialProjectForm(forms.ModelForm):

    class Meta:
        model = PotentialProject
        fields = ('name', 'description', 'reason', 'profit_opportunities')


class InspirationForm(forms.ModelForm):

    class Meta:
        model = Inspiration
        fields = ('name', 'image')


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('client', 'project_name', 'price', 'payment_status', 'completion_status')


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name', 'email', 'phone_number')
