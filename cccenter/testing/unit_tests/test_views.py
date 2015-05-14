from django.test import TestCase
from cccenter.views import *
import mock

class TestViews(TestCase):
    
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_update_notifications_Pass1(self, mock_shortcuts, mock_notify):
        mock_shortcuts.user = 'user'
        mock_shortcuts.GET.get.return_value = 'note'
        
        update_notifications(mock_shortcuts)
        
        self.assertTrue(mock_shortcuts.GET.get.called)
        mock_notify.viewed_notification.assert_called_with('user', 'note')
