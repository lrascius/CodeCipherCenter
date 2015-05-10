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

    @mock.patch('cccenter.python.notification.Notification')
    def test_unviewed_notification(self, mock_notification):
        mock_notification.objects.filter.return_value = mock_notification
        
        res = unviewed_notifications('user')
        
        self.assertFalse(res)
        mock_notification.objects.filter.assert_called_with(user='user', viewed=False)
        
    @mock.patch('cccenter.python.notification.Notification')
    def test_unviewed_notification2(self, mock_notification):
        mock_notification.objects.filter.return_value = [0, 0]
        
        res = unviewed_notifications('user')
        
        self.assertTrue(res)
        mock_notification.objects.filter.assert_called_with(user='user', viewed=False)
        
    @mock.patch('cccenter.python.notification.Notification')
    def test_viewed_notification_Pass1(self, mock_notification):
        mock_notification.objects.filter.return_value = [mock_notification]
        mock_notification.id = 1
        
        res = viewed_notification('user', 1)
        
        self.assertTrue(res)
        self.assertTrue(mock_notification.viewed)
        self.assertTrue(mock_notification.save.called)
