from __future__ import unicode_literals

from django.db import models


class Job(models.Model):
    Paid = 'Paid'
    Unpaid = 'Unpaid'
    Yes = 'Yes'
    No = 'No'

    enum = (
        (Paid , 'Paid'),
        (Unpaid, 'Unpaid'),
    )

    enum2 = (
        (Yes, 'Yes'),
        (No, 'No'),
    )

    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=20, null=False, blank=False)
    colour = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateField(auto_now_add=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(max_length=20, null=False, blank=False, choices=enum)
    completion_status = models.CharField(max_length=20, null=False, blank=False, choices=enum2)

    def __unicode__(self):
        return self.project_name


class Client(models.Model):

    name = models.CharField(max_length=20, null=False, blank=False)
    email = models.CharField(max_length=20, null=False, blank=False)
    phone_number = models.DecimalField(max_digits=11, decimal_places=0)

    def __unicode__(self):
        return self.name


class PotentialClient(models.Model):

    email = 'email'
    phone_number = 'Phone Number'
    social_media = 'Social media'

    choices = (
                (email, 'email'),
                (phone_number, 'Phone Number'),
                (social_media, 'Social media')
    )
    name = models.CharField(max_length=20, null=False, blank=False)
    reason = models.TextField(max_length=140, null=True)
    how_to_get_client = models.TextField(max_length=140, null=True)
    best_way_to_contact = models.CharField(max_length=20, null=False, blank=False, choices=choices)

    def __unicode__(self):
        return self.name


class PotentialProject(models.Model):

    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(max_length=140, null=True)
    reason = models.TextField(max_length=140, null=True)
    profit_opportunities = models.CharField(max_length=140, null=True, blank=True)

    def __unicode__(self):
        return self.name


class DesignProblems(models.Model):

    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(max_length=140, null=True)
    potential_solution = models.TextField(max_length=140, null=True)
    profit_opportunities = models.CharField(max_length=140, null=True, blank=True)

    def __unicode__(self):
        return self.name





