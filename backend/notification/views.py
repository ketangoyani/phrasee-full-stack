from django.db.models import Count
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from notification.utils import generate_aggregated_notifications

class NotificationAPIView(GenericAPIView):
    def get(self, request):
        data = generate_aggregated_notifications()
        return Response({"results": data})