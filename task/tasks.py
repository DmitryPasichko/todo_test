from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_invitation_emails(user_emails, title):
    """
    Delayed ivent of sending invitation emails to list of emails
    :param user_emails:
    :param title:
    :return:
    """
    email_list = ",".join(user_emails)
    for email in user_emails:
        send_mail(
            f"task '{title}' has been updated.",
            f"Users that are subscribed:'{email_list}'",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
        )
