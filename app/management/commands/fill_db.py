import json
import os

from django.core.management.base import BaseCommand

from app.models import Client, Mailing


class Command(BaseCommand):

    help = "Fill database with test data"

    def handle(self, *args, **options):

        # Creating clients objects
        clients = open("./app/fixtures/clients.json", "r")
        clients_data = json.load(clients)

        clients_list = []

        for dt in clients_data:
            clients_list.append(Client(**dt))

        Client.objects.bulk_create(clients_list)

        # Creating mailing objects
        mailings = open("./app/fixtures/mailing.json", "r")
        mailings_data = json.load(mailings)

        mailings_list = []
        for ml in mailings_data:
            mailings_list.append(Mailing(**ml))

        Mailing.objects.bulk_create(mailings_list)

