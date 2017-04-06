from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from OGT import settings
from constants import ResponseMessages, Status
from dashboard.libs.utils import UserProfileHelper


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.DecimalField(max_digits=11, decimal_places=0, null=True, blank=True)

    def get_split_address(self):
        return UserProfileHelper.get_split_user_address(self.address)

    def __unicode__(self):
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
        (No, 'No')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=20, null=False)
    items = models.TextField(max_length=300, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True, null=False, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    payment_status = models.CharField(max_length=20, null=True, choices=enum)
    completion_status = models.CharField(max_length=20, null=True, blank=True, choices=enum2)

    def __unicode__(self):
        return self.project_name


class Client(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    phone_number = models.DecimalField(max_digits=11, decimal_places=0, null=True, blank=True)
    # total_amount_paid = models.DecimalField(max_digits=15, decimal_places=2)

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    reason = models.TextField(max_length=140, null=True)
    how_to_get_client = models.TextField(max_length=140, null=True)
    best_way_to_contact = models.CharField(max_length=20, null=False, blank=False, choices=choices)

    def __unicode__(self):
        return self.name


class PotentialProject(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, blank=False)
    description = models.TextField(max_length=140, null=True)
    reason = models.TextField(max_length=140, null=True)
    profit_opportunities = models.CharField(max_length=140, null=True, blank=True)

    def __unicode__(self):
        return self.name


class DesignProblems(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, blank=False)
    description = models.TextField(max_length=140, null=True)
    potential_solution = models.TextField(max_length=140, null=True)
    profit_opportunities = models.CharField(max_length=140, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Inspiration(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.FileField(upload_to='inspiration/%Y/%m/%d')

    def __unicode__(self):
        return self.name


class Task(models.Model):

    status_choices = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('Client Review', 'Client Review'),
    )

    yes_no = (
        ('yes', 'Yes'),
        ('no', 'No')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, blank=False)
    description = models.CharField(max_length=140, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, blank=False, choices=status_choices)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=False, blank=False)
    archived = models.CharField(max_length=10, null=False, blank=False, choices=yes_no, default="no")
    archived_at = models.DateField(auto_now_add=False, null=True, blank=True)

    @classmethod
    def getAllProjectsAndTheirTasks(cls, user):

        all_tasks = cls.objects.select_related().filter(user=user, archived="no")
        all_jobs = Job.objects.filter(user=user)

        jobs_aggregation = []

        if len(all_jobs) > 0:
            for job in all_jobs:
                # Append (job_object, no_of_tasks, no_of_completed_tasks)
                total_tasks = len(all_tasks.filter(job=job.id))
                total_completed_tasks = len(all_tasks.filter(job=job.id, status=Status.completed))
                total_uncompleted_tasks = total_tasks - total_completed_tasks
                jobs_aggregation.append([job, total_tasks, total_completed_tasks, total_uncompleted_tasks])

            response = {"status": "success", "data": jobs_aggregation}
            return response

        else:
            response = {"status": "error", "message": ResponseMessages.NO_JOBS_FOUND}
            return response

    def __unicode__(self):
        return str(self.description)


class ItemPrice(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False, blank=False)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=140, null=True, blank=True)

    def __unicode__(self):
        return self.name


class ErrorLogModel(models.Model):
    """
    Logs all errors.
    """

    error_message = models.CharField(max_length=100, null=False, blank=False)
    calling_function = models.CharField(max_length=100, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return str(self.date_added) + ' ' + str(self.error_message) + ' - Function:' + str(self.calling_function)


class SentEmailsLog(models.Model):

    choices = (
        ('No', 'NO'),
        ('Yes', 'YES')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_email = models.EmailField(max_length=30, null=False, blank=False)
    to_email = models.EmailField(max_length=30, null=False, blank=False)
    host_email = models.EmailField(max_length=30, null=False, blank=False)
    attachments = models.CharField(max_length=5, choices=choices)
    attachment_type = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return 'User: ' + str(self.user.username) + ' - mail_to:' + str(self.to_email)
