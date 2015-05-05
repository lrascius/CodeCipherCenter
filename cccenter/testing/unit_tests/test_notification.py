from django.test import TestCase
from cccenter.python.notification import *
import mock

class TestNotification(TestCase):

    @mock.patch('cccenter.python.notification.Notification')
    def test_notification_filters_by_user(self, mock_notification):
        mock_notification.objects.filter.return_value = mock_notification
        
        res = get_notifications('user')
        
        self.assertEqual(res, mock_notification)
        mock_notification.objects.filter.assert_called_with(user='user')        

    def test_unviewed_notification(self):
        user = mock.Mock()
        notification = mock.Mock(spec=models.Notification)
        models.Notification.get_notifications(notification, user)
        notification = notification.filter.assert_called_with(user=user) 
        self.assertTrue(len(notification) != 0)
