from core.models import Notification
import requests


def default(request):
    try:
        notifications = Notification.objects.filter(user=request.user).order_by("-id")[:10]
    except:
        notifications = None

    return {
        "notifications":notifications,
       
    }