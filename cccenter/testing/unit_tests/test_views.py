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
                   "active":"home"}
                  
        self.assertEqual(res, "home_page")
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/home_page.html', context)
        mock_mail.send_mail.assert_called_with('mail', 'mail', 'mail', ['admin@cccenter.com'])
        
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
                   "active":"home"}
                  
        self.assertEqual(res, "home_page")
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/home_page.html', context)
        
    @mock.patch('cccenter.views.mail')
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_home_Pass3(self, mock_shortcuts, mock_notify, mock_mail):
        mock_shortcuts.render.return_value = "home_page"
        mock_shortcuts.POST.get.return_value = False
        mock_shortcuts.user.is_anonymous.return_value = False
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unread'
        mock_shortcuts.method = 'GET'
        
        res = home(mock_shortcuts)
        
        context = {"notifications":"notify",
                   "unseen_notification":"unread",
                   "title":"Code and Cipher Center",
                   "active":"home"}
                  
        self.assertEqual(res, "home_page")
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/home_page.html', context)
        
    @mock.patch('cccenter.views.json')
    @mock.patch('cccenter.views.random')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.cf')
    @mock.patch('cccenter.views.general')
    @mock.patch('cccenter.views.HttpResponse')
    def test_getCipher_Pass1(self, mock_response, mock_general, mock_cf, mock_shortcuts, mock_random, mock_json):
        mock_general.generate_paragraph.return_value = 'text'
        mock_cf.caesar_shift_encode.return_value = 'cipher'
        mock_response.return_value = 'response'
        mock_random.randint.return_value = 1
        mock_json.dumps.return_value = 'json'
        
        res = getCipher(mock_shortcuts)
        
        self.assertEqual(res, 'response')
        self.assertTrue(mock_general.generate_paragraph.called)
        mock_cf.caesar_shift_encode.assert_called_with('text', 1)
        mock_response.assert_called_with('json', content_type="application/json")
        
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_create_challenge_Pass1(self, mock_shortcuts, mock_notify):
        mock_shortcuts.method = "GET"
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        
        res = create_challenge(mock_shortcuts)
        
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/create_challenge.html',
                                                 {"title":"Code and Cipher Center", "active":"newchallenge",
                                                  "notifications" : 'notify',
                                                  "unseen_notification" : 'unseen'
                                                 })
                                        
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.Cipher')
    @mock.patch('cccenter.views.general')         
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_create_challenge_Pass2(self, mock_shortcuts, mock_notify, mock_general, mock_cipher, mock_user):
        mock_shortcuts.method = "POST"
        mock_shortcuts.POST.getlist.return_value = []
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        
        res = create_challenge(mock_shortcuts)
        
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/create_challenge.html',
                                                 {"title":"Code and Cipher Center", "active":"newchallenge",
                                                  "bool":True, "error":"Challenge type is required",
                                                  "notifications":'notify',
                                                  "unseen_notification":'unseen'
                                                 })
