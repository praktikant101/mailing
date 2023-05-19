from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Mailing
from app.serializers import MailingSerializer


class MailingTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_method(self):

        data = {"created_at": "2023-05-16T10:42:19.386Z",
                "body": "Hello, World!",
                "tag": "test",
                "operator_code": 90}
        serializer = MailingSerializer(data=data)
        serializer.is_valid()
        response = serializer.create(serializer.validated_data)
        self.assertEqual(type(response), Mailing)