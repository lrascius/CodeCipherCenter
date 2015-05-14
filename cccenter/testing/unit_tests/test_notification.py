from django.test import TestCase
from cccenter.python.notification import *
import mock

class TestNotification(TestCase):

    @mock.patch('cccenter.python.notification.Notification')
    def test_notification_filters_by_user_Pass1(self, mock_notification):
        mock_notification.objects.filter.return_value = mock_notification
        mock_notification.order_by.return_value = [mock_notification]
        
        res = get_notifications('user')
        
        self.assertEqual(res, [mock_notification])
        mock_notification.objects.filter.assert_called_with(user='user')   
        
    @mock.patch('cccenter.python.notification.Notification')
    def test_notification_filters_by_user_Pass2(self, mock_notification):
        mock_notification.objects.filter.return_value = mock_notification
        mock_notification.order_by.return_value = [mock_notification]
        
        res = get_notifications('user', get_all=True)
        
        self.assertEqual(res, [mock_notification])
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
        self.assertTrue(mock_notification.viewed)
        self.assertTrue(mock_notification.save.called)

    @mock.patch('cccenter.python.notification.timezone')
    @mock.patch('cccenter.python.notification.Challenge')
    @mock.patch('cccenter.python.notification.Notification')
    def test_solved_cipher_notification(self, mock_notification, mock_challenge, mock_timezone):
        mock_challenge.objects.filter.return_value = [mock_notification]
        mock_notification.users.all.return_value = [mock_timezone]
        mock_notification.solved_by.all.return_value = [mock_timezone]
        mock_notification.username = 'username'
        mock_notification.challenge_id = 1
        mock_timezone.now.return_value = 'now'
        mock_timezone.username = 'name'
        mock_notification.return_value = mock_notification
        
        solved_cipher_notification('username', 1)
        
        mock_notification.assert_called_with(user=mock_timezone, notification='username has solved challenge # 1',
                                             link='/cipher/challengepage/?challenge_id=1', datetime='now')
        self.assertTrue(mock_notification.save.called)
