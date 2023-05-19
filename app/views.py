from rest_framework import generics, viewsets

from .serializers import ClientSerializer, MailingSerializer, MailingStatsSerializer
from .models import Client, Mailing, MailingStats


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingStatsList(generics.ListAPIView):
    queryset = MailingStats.objects.all()
    serializer_class = MailingStatsSerializer


class MailingStatsDetail(generics.RetrieveAPIView):
    queryset = MailingStats.objects.all()
    serializer_class = MailingStatsSerializer


class MessageList(generics.ListAPIView):
    queryset = MailingStats.objects.all()
    serializer_class = MailingStatsSerializer


class MessageDetail(generics.RetrieveAPIView):
    queryset = MailingStats.objects.all()
    serializer_class = MailingStatsSerializer


