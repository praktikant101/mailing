from datetime import datetime, timedelta
from decouple import config

from django.core.mail import send_mail

from celery.result import AsyncResult
from celery import shared_task

from main.celery import app
from app.service.mailing import send_mailing


from app.models import Mailing, MailingStats


@app.task
def send_postponed_mailing(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)
    send_mailing(mailing)


@app.task
def update_messages_stats(task_id, mailing_id):

    mailing = Mailing.objects.get(pk=mailing_id)

    task_result = AsyncResult(task_id, app=app)

    if task_result.ready():
        completion_time = datetime.now()
        mailing.sent_at = completion_time
        mailing.save()
        stats_table = MailingStats.objects.get(mailing_id=mailing.id)
        stats_table.completed = True
        stats_table.save()


# sending out mailings executed 24 hours ago
@shared_task
def send_mailing_stats():
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    mailings = MailingStats.objects.filter(mailing__created_at__gte=twenty_four_hours_ago)

    email_address = config("EMAIL")

    if not email_address:
        return None

    if not mailings:
        return None

    email_body = "Stats:\n\n"

    for mail in mailings:
        mail_url = f"http://0.0.0.0:8000/stats/{mail.id}"
        mail_text = f"Mail ID: {mail.id}\n"
        email_body += mail_text + mail_url + "\n\n"

    send_mail("Mailings stats",
              email_body,
              "admin@localhost",
              [email_address],
              fail_silently=False)


