from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_task_update_notification(task_id):
    print(f"Task {task_id} has been updated!")
    # Optionally, send an email (configure email backend in settings.py)
    # send_mail(
    #     'Task Updated',
    #     f'Task {task_id} has been updated.',
    #     'from@example.com',
    #     ['to@example.com'],
    #     fail_silently=False,
    # )