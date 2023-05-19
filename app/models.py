from django.db import models


class Client(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=20, blank=True, null=True)
    tz = models.CharField(default='UTC', max_length=20)

    def __str__(self):
        return self.phone_number


class Mailing(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    body = models.TextField()
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.pk


class Message(models.Model):
    sent_at = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, default=None, blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.pk


class ClientMessage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.pk


class MailingStats(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='stats')
    no_messages = models.IntegerField(default=0)
    no_messages_ok = models.IntegerField(default=0)
    no_messages_fail = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
