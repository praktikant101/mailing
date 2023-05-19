from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Client, Mailing


class ClientTestCase(APITestCase):

    def setUp(self):

        client = Client(phone_number="+998900234567")
        client.save()

    def test_client_list(self):

        response = self.client.get(reverse("clients"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_create(self):

        url = reverse("clients")
        response = self.client.post(url, {"phone_number": "+998900234566", "tag": "hello", "tz": "UTC"}, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_retrieve(self):

        client = Client.objects.first()
        response = self.client.get(reverse("client", kwargs={"pk": client.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_update(self):

        client = Client.objects.first()
        response = self.client.put(reverse("client", kwargs={"pk": client.id}),
                                   {"phone_number": "+998900234566", "tag": "hello", "tz": "UTC"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        self.assertEqual(client.phone_number, "+998900234566")