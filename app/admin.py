from django.contrib import admin

from .models import Client, Mailing, Message, ClientMessage, MailingStats

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(ClientMessage)
admin.site.register(MailingStats)
