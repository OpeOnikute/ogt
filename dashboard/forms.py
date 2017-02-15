from django import forms
from .models import DesignProblems, PotentialClient, PotentialProject, Inspiration


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

