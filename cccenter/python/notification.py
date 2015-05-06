from cccenter.models import Notification

def get_notifications(user, get_all):
    '''If get_all is true, grabs all the user notifications sorted by date
       Else, grabs the 5 most recent user notifications'''
    if get_all == True:
        notifications = Notification.objects.filter(user=user).order_by('-datetime')
    else:
        notifications = Notification.objects.filter(user=user).order_by('-datetime')[:5]
    return notifications

def unviewed_notifications(username):
    '''Checks if there is any unviewed notifications for a user'''
    notifications = Notification.objects.filter(user=username, viewed=False)
    if (len(notifications) != 0):
        return True
    else:
        return False

def viewed_notification(username, notification_id):
    '''Sets the notification as viewed when a user clicks on it'''
    notifications = Notification.objects.filter(user=username, viewed=False)

    for notification in notifications:
        if(int(notification.id) == int(notification_id)):
            notification.viewed = True
            notification.save()
            return True

    return False