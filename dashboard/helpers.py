from .models import Job, Task
from constants import Status, ResponseMessages


class ProjectsHelper(object):

    def __init__(self):
        self.name = "ProjectsHelperClass"

    @classmethod
    def getAllProjectsAndTheirTasks(cls, user):

        all_tasks = Task.objects.select_related()
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

