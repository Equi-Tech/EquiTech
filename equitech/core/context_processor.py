from core.models import Notification

def default(requset):
    try:
        notifications = Notification.objects.filter(user = requset.user).order_by("-id")[:10]
    except:
        notifications = None
    return {
        "notifications":notifications,
    }