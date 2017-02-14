from django.contrib import admin
from .models import Job, Client, PotentialClient, DesignProblems, PotentialProject, Inspiration

admin.site.register(Job)
admin.site.register(Client)
admin.site.register(PotentialClient)
admin.site.register(DesignProblems)
admin.site.register(PotentialProject)
admin.site.register(Inspiration)
