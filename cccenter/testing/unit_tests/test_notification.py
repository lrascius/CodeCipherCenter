from django.test import TestCase
from cccenter.models import *
import mock

class TestNotification(TestCase):

    def test_notification_filters_by_user(self):
        user = mock.Mock()
        notification = mock.Mock(spec=models.Notification)
        models.Notification.get_notifications(notification, user)
        notification.filter.assert_called_with(user=user)        

    def test_unviewed_notification(self):
        user = mock.Mock()
        notification = mock.Mock(spec=models.Notification)
        models.Notification.get_notifications(notification, user)
        notification = notification.filter.assert_called_with(user=user) 
        self.assertTrue(len(notification) != 0)