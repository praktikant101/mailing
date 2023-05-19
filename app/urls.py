from django.urls import path

from .views import (
    ClientViewSet,
    MailingViewSet,
    MailingStatsList,
    MailingStatsDetail,
    MessageList,
)

urlpatterns = [
    # clients
    path("clients/", ClientViewSet.as_view({"get": "list", "post": "create"}), name="clients"),
    path("clients/<int:pk>", ClientViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
         name="client"),

    # mailings
    path("mailings/", MailingViewSet.as_view({"get": "list", "post": "create"}), name="mailings"),
    path("mailings/<int:pk>", MailingViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
         name="mailing"),

    # messages
    path("messages/", MessageList.as_view(), name="messages"),
    path("messages/<int:pk>", MessageList.as_view(), name="message"),

    # stats
    path("stats/", MailingStatsList.as_view(), name="stats"),
    path("stats/<int:pk>", MailingStatsDetail.as_view(), name="stat"),
]
