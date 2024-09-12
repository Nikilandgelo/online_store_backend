import os
from celery import shared_task
from django.core.mail import send_mail, get_connection
from celery.exceptions import MaxRetriesExceededError


@shared_task(bind=True, name='User.tasks.send_email', max_retries=12)
def send_email(self, title: str, html_message: str, email: str = None,
               mail_for_admin: bool = False) -> None:

    # kwargs passing to default backend (backends.smtp.EmailBackend)
    # because i dont pass custom
    custom_connection = get_connection(
        host=os.getenv('EMAIL_HOST'), port=os.getenv('EMAIL_PORT'),
        username=os.getenv('EMAIL_HOST_USER'),
        password=os.getenv('EMAIL_HOST_PASSWORD'),
        use_tls=True, use_ssl=False)

    try:
        if mail_for_admin:
            email = os.getenv('ADMIN_EMAIL')
        send_mail(title, '', os.getenv('EMAIL_HOST_USER'),
                  recipient_list=[email], connection=custom_connection,
                  html_message=html_message)
    except Exception as error:
        retry_count = self.request.retries or 0
        retry_timer = 5 * (1.5 * retry_count)
        print(f'{error}\nRetrying after {retry_timer}s...')
        try:
            self.retry(exc=error, countdown=retry_timer)
        except MaxRetriesExceededError as err:
            print(f'Task failed after maximum retries: {err}')
