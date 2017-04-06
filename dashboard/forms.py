from django import forms
from django.contrib.auth.models import User
from .models import Job, DesignProblems, PotentialClient, PotentialProject, Inspiration, Client, Task, ItemPrice, Profile


class SignUpForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('address', 'phone_number')


class DesignProblemsForm(forms.ModelForm):

    class Meta:
        model = DesignProblems
        fields = ('user', 'name', 'description', 'potential_solution', 'profit_opportunities')


class PotentialClientForm(forms.ModelForm):

    class Meta:
        model = PotentialClient
        fields = ('user', 'name', 'reason', 'how_to_get_client', 'best_way_to_contact')


class PotentialProjectForm(forms.ModelForm):

    class Meta:
        model = PotentialProject
        fields = ('user', 'name', 'description', 'reason', 'profit_opportunities')


class InspirationForm(forms.ModelForm):

    class Meta:
        model = Inspiration
        fields = ('user', 'name', 'image')


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('user', 'client', 'project_name', 'price', 'payment_status', 'completion_status')


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('user', 'name', 'email', 'phone_number')


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('user', 'description', 'status', 'job')


class ItemPriceForm(forms.ModelForm):

    class Meta:
        model = ItemPrice
        fields = ('user', 'name', 'price', 'description')
