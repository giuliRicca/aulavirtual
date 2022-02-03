from .models import Notification
from django.core import serializers
import json


def notification_loader(request):
    context = {}
    try:
        notifications = Notification.objects.filter(
            recipient=request.user, read=False)
        serialized_data = serializers.serialize(
            "json", notifications, fields=('pk', 'message', 'created_at'))
        print(serialized_data)
        context['notifications'] = serialized_data
        context['notifications_count'] = 0
    except:
        pass

    return context
