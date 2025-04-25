from celery import shared_task
from django.core.mail import send_mail
from core.models import Task

@shared_task
def send_task_update_notification(task_id):
    try:
        # Fetch the task and its assignee
        task = Task.objects.get(id=task_id)
        assignee = task.assignee
        if assignee and assignee.email:
            # Send email to the assignee
            subject = f'Task Updated: {task.title}'
            message = f'The task "{task.title}" has been updated.\n\n' \
                      f'Description: {task.description}\n' \
                      f'Status: {task.status}\n' \
                      f'Deadline: {task.deadline}\n' \
                      f'Updated At: {task.updated_at}'
            from_email = 'chuksoclock@gmail.com'
            recipient_list = [assignee.email]
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        else:
            print(f"No assignee or email found for task {task_id}")
    except Task.DoesNotExist:
        print(f"Task {task_id} not found")
    except Exception as e:
        print(f"Error sending email for task {task_id}: {str(e)}")
        raise