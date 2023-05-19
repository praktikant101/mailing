from rest_framework import serializers

from app.models import ClientMessage, Message
from .general import ProcessDataError


def create_message(data, mailing):
    message_objects = []
    message_client_objects = []

    try:
        for dt in data:
            message = Message(status=dt["message"],
                              sent_at=dt["time"],
                              mailing=mailing)
            message_objects.append(message)

            message_client = ClientMessage(client=dt["client"],
                                           message=message)
            message_client_objects.append(message_client)

        Message.objects.bulk_create(message_objects)
        ClientMessage.objects.bulk_create(message_client_objects)

    except ProcessDataError as e:
        serializers.ValidationError(str(e))

    return True
