import datetime
import json
from decouple import config
import aiohttp
import asyncio

from django.db.models import Q
from rest_framework import serializers

from app.models import Client
from .general import ProcessDataError
from .messaging import create_message
from .stats import collect_stats

message_url = 'https://probe.fbrq.cloud/v1/send/'

token = config('TOKEN')

headers = {"Accept": "application/json",
           "Authorization": f"Bearer {token}",
           "Content-Type": "application/json"}


class MailingService:
    clients = []
    sending_data = []
    message_url = ""
    response_data = []
    sent_at = None

    def __init__(self, mailing):
        self.mailing = mailing
        self.mailing_id = self.mailing.id
        self.mailing_tag = self.mailing.tag
        self.mailing_operator_code = self.mailing.operator_code
        self.body = self.mailing.body
        self.created_at = self.mailing.created_at
        self.sending_data = self.get_sending_data()
        self.clients = self.get_clients()
        self.message_url = self.get_message_url()

    def get_message_url(self):
        if not self.message_url:
            self.message_url = message_url + str(self.mailing_id)
        return self.message_url

    def get_clients(self):
        if self.clients:
            return self.clients

        if not self.mailing_tag and not self.mailing_operator_code:
            self.clients = list(Client.objects.all())

        elif not self.mailing_tag or not self.mailing_operator_code:
            self.clients = list(Client.objects.filter(
                Q(tag=self.mailing_tag) | Q(operator_code=self.mailing_operator_code))
            )

        else:
            self.clients = list(Client.objects.filter(
                tag=self.mailing_tag, operator_code=self.mailing_operator_code)
            )

        return self.clients

    def get_client_by_phone_number(self, phone_number):
        for client in self.clients:
            if client.phone_number == phone_number:
                return client

            return None

    def get_sending_data(self):

        if not self.sending_data:
            for client in self.clients:
                self.sending_data.append({
                    "id": self.mailing_id,
                    "phone": client.phone_number,
                    "text": self.mailing.body,
                    "client": client,
                })

        return self.sending_data

    # Sending a mailing asynchronously
    async def arrange_sending(self, session, data):

        # preparing data
        try:
            data_sending = {key: data[key] for key in data.keys() if key != "client"}

            async with session.post(self.message_url, data=json.dumps(data_sending), headers=headers) \
                    as request:
                response_data = await request.json()
                time_completed = datetime.datetime.now()
                response_data["phone"] = data["phone"]
                response_data["time"] = time_completed
                response_data["client"] = data["client"]
                return response_data

        except ProcessDataError as e:
            raise serializers.ValidationError(str(e))

    # Sending messages within mailing asynchronously
    async def send_mailing(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for data in self.sending_data:
                task = asyncio.create_task(self.arrange_sending(session, data))
                tasks.append(task)

            self.response_data = await asyncio.gather(*tasks)
            return self.response_data


def send_mailing(mailing):
    loop = asyncio.new_event_loop()
    mailing_service = MailingService(mailing)
    mailing_service.get_sending_data()
    response_data = loop.run_until_complete(mailing_service.send_mailing())
    loop.close()

    try:
        create_message(response_data, mailing)
        collect_stats(response_data, mailing)

    except ProcessDataError as e:
        raise serializers.ValidationError(str(e))

    return response_data
