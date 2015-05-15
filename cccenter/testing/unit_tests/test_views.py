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
        
    @mock.patch('cccenter.views.mail')
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_home_Pass1(self, mock_shortcuts, mock_notify, mock_mail):
        mock_shortcuts.render.return_value = "home_page"
        mock_shortcuts.POST.get.return_value = 'mail'
        mock_shortcuts.user.is_anonymous.return_value = False
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unread'
        mock_shortcuts.method = 'POST'
        
        res = home(mock_shortcuts)
        
        context = {"message":"Thank you, your message has been sent.",
                   "notifications":"notify",
                   "unseen_notification":"unread",
                   "title":"Code and Cipher Center",
                   "active":"home"
                  }
                  
        self.assertEqual(res, "home_page")
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/home_page.html', context)
        
    @mock.patch('cccenter.views.mail')
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_home_Pass2(self, mock_shortcuts, mock_notify, mock_mail):
        mock_shortcuts.render.return_value = "home_page"
        mock_shortcuts.POST.get.return_value = False
        mock_shortcuts.user.is_anonymous.return_value = False
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unread'
        mock_shortcuts.method = 'POST'
        
        res = home(mock_shortcuts)
        
        context = {"message":"Please make sure all fields are filled.",
                   "notifications":"notify",
                   "unseen_notification":"unread",
                   "title":"Code and Cipher Center",
                   "active":"home"
                  }
                  
        self.assertEqual(res, "home_page")
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/home_page.html', context)
