from celery import shared_task

print("Loading send_task_update_notification task")  # Debug

@shared_task
def send_task_update_notification(task_id):
    try:
        print(f"Starting task for task_id: {task_id}")  # Debug
        print(f"Task {task_id} has been updated!")
        print(f"Completed task for task_id: {task_id}")  # Debug
    except Exception as e:
        print(f"Error in send_task_update_notification for task_id {task_id}: {str(e)}")
        raise  # Re-raise to ensure Celery logs the error