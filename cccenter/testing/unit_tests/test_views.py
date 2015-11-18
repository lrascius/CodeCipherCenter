from django.test import TestCase
from cccenter.views import *
import mock

def create_challenge_pass3_side_effect(group):
    if group == 'challengetype':
        return ['single']
    elif group == 'radiogroup':
        return []
    elif group == 'cipher':
        return []
        
def create_challenge_pass4_side_effect(group):
    if group == 'challengetype':
        return ['single']
    elif group == 'radiogroup':
        return ['easy']
    elif group == 'cipher':
        return []
        
def create_challenge_pass5_side_effect(group):
    if group == 'challengetype':
        return ['single']
    elif group == 'radiogroup':
        return []
    elif group == 'cipher':
        return ['easy']
        
def check_plaintext_pass2_side_effect(inp, p):
    if inp == 'challenge_id':
        return '0'
    elif  inp == 'guessed_plaintext':
        return 'text'
        
def challenge_page_pass1_side_effect(inp):
    if inp == 'username':
        return ['name']
    elif inp == 'challenge_id':
        return ['0']
        
def auth_view_pass1_side_effect(inp, s):
    if inp == 'username':
        return 'name'
    elif inp == 'password':
        return 'pass'

def auth_view_pass2_side_effect(inp, s):
    if inp == 'username':
        return 'name'
    elif inp == 'password':
        return 'pass'
        
def settings_pass1_side_effect(inp, s):
    if inp == 'first_name':
        return 'first'
    elif inp == 'last_name':
        return 'last'
    elif inp == 'email':
        return 'email'

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
        mock_shortcuts.render.return_value = True
        
        res = create_challenge(mock_shortcuts)
        
        self.assertTrue(res)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/create_challenge.html',
                                                 {"title":"Code and Cipher Center", "active":"newchallenge",
                                                  "notifications" : 'notify',
                                                  "unseen_notification" : 'unseen'
                                                 })
                                        
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_create_challenge_Pass2(self, mock_shortcuts, mock_notify):
        mock_shortcuts.method = "POST"
        mock_shortcuts.POST.getlist.return_value = []
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_shortcuts.render.return_value = True
        
        res = create_challenge(mock_shortcuts)
        
        self.assertTrue(res)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/create_challenge.html',
                                                 {"title":"Code and Cipher Center", "active":"newchallenge",
                                                  "bool":True, "error":"Challenge type is required",
                                                  "notifications":'notify',
                                                  "unseen_notification":'unseen'
                                                 })
    
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_create_challenge_Pass3(self, mock_shortcuts, mock_notify):
        mock_shortcuts.method = "POST"
        mock_shortcuts.POST.getlist.side_effect = create_challenge_pass3_side_effect
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_shortcuts.render.return_value = True
        
        res = create_challenge(mock_shortcuts)
        
        self.assertTrue(res)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/create_challenge.html',
                                                 {"title":"Code and Cipher Center", "active":"newchallenge",
                                                  "bool":True, "error":"Select by difficulty or list of ciphers",
                                                  "notifications":'notify',
                                                  "unseen_notification":'unseen'
                                                 })
                                                 
    # @mock.patch('cccenter.views.User')
    # @mock.patch('cccenter.views.Cipher')
    # @mock.patch('cccenter.views.random')
    # @mock.patch('cccenter.views.HttpResponseRedirect')
    # @mock.patch('cccenter.views.cf')
    # @mock.patch('cccenter.views.general')         
    # @mock.patch('cccenter.views.notify')
    # @mock.patch('cccenter.views.shortcuts')
    # def test_create_challenge_Pass4(self, mock_shortcuts, mock_notify, mock_general, mock_cf, mock_redirect,
    #                                 mock_random, mock_cipher, mock_user):
    #     mock_shortcuts.method = "POST"
    #     mock_shortcuts.POST.getlist.side_effect = create_challenge_pass4_side_effect
    #     mock_general.generate_paragraph.return_value = 'text'
    #     mock_cipher.objects.all.return_value = mock_cipher
    #     mock_cipher.filter.return_value = [mock_cipher]
    #     mock_cipher.ciphertype = 'easy'
    #     mock_random.randint.return_value = 0
    #     mock_cf.create_ciphertext.return_value = {"ciphertext":'cipher', "cipherkey":'key'}
    #     mock_user.objects.get.return_value = mock_user
    #     mock_cf.create_challenge.return_value = {'challenge_id':1}
    #     mock_redirect.return_value = True
        
    #     res = create_challenge(mock_shortcuts)
        
        # self.assertTrue(res)
        # self.assertTrue(mock_random.randint.called)
        # mock_cf.create_challenge.assert_called_with('text', 'cipher', 'easy', 'key', 'single', [mock_user])
        # mock_redirect.assert_called_with('/cipher/challengepage/?challenge_id=1')
        
    # @mock.patch('cccenter.views.User')
    # @mock.patch('cccenter.views.HttpResponseRedirect')
    # @mock.patch('cccenter.views.cf')
    # @mock.patch('cccenter.views.general')         
    # @mock.patch('cccenter.views.notify')
    # @mock.patch('cccenter.views.shortcuts')
    # def test_create_challenge_Pass5(self, mock_shortcuts, mock_notify, mock_general, mock_cf, mock_redirect, mock_user):
    #     mock_shortcuts.method = "POST"
    #     mock_shortcuts.POST.getlist.side_effect = create_challenge_pass5_side_effect
    #     mock_general.generate_paragraph.return_value = 'text'
    #     mock_cf.create_ciphertext.return_value = {"ciphertext":'cipher', "cipherkey":'key'}
    #     mock_user.objects.get.return_value = mock_user
    #     mock_cf.create_challenge.return_value = {'challenge_id':1}
    #     mock_redirect.return_value = True
        
    #     res = create_challenge(mock_shortcuts)
        
    #     self.assertTrue(res)
    #     mock_cf.create_challenge.assert_called_with('text', 'cipher', 'easy', 'key', 'single', [mock_user])
    #     mock_redirect.assert_called_with('/cipher/challengepage/?challenge_id=1')
        
    @mock.patch('cccenter.views.Http404')
    @mock.patch('cccenter.views.shortcuts')
    def test_check_plaintext_Pass1(self, mock_shortcuts, mock_404):
        mock_shortcuts.method = "GET"
        mock_404.return_value = mock_404
        
        res = check_plaintext(mock_shortcuts)
        
        self.assertEqual(res, mock_404)
        
    @mock.patch('cccenter.views.Http404')
    @mock.patch('cccenter.views.HttpResponse')
    @mock.patch('cccenter.views.json')
    @mock.patch('cccenter.views.cf')
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    def test_check_plaintext_Pass2(self, mock_shortcuts, mock_notify, mock_cf, mock_json, mock_response, mock_404):
        mock_shortcuts.method = "POST"
        mock_shortcuts.POST.get.side_effect = check_plaintext_pass2_side_effect
        mock_shortcuts.user.id = 1
        mock_shortcuts.user.username = 'name'
        mock_cf.check_solution.return_value = True
        mock_notify.solved_cipher_notification.return_value = 'note'
        mock_json.dumps.return_value = 'json'
        mock_response.return_value = mock_response
        
        res = check_plaintext(mock_shortcuts)
        
        self.assertEqual(res, mock_response)
        mock_cf.check_solution.assert_called_with(0, 1, 'text')
        mock_notify.solved_cipher_notification('name', '0')
        mock_json.dumps.assert_called_with({'success':True})
        mock_response.assert_called_with('json', content_type="application/json")
        
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.Notification')
    @mock.patch('cccenter.views.timezone')
    @mock.patch('cccenter.views.HttpResponseRedirect')
    def test_challenge_page_Pass1(self, mock_redirect, mock_timezone, mock_notification, mock_user, mock_shortcuts):
        mock_shortcuts.method = 'POST'
        mock_shortcuts.POST.getlist = challenge_page_pass1_side_effect
        mock_shortcuts.user = mock_user
        mock_user.objects.get.return_value = mock_user
        mock_timezone.now.return_value = 'now'
        mock_notification.return_value = mock_notification
        mock_redirect.return_value = mock_redirect
        mock_shortcuts.META.get.return_value = 'hi'
        mock_user.username = 'name1'
        mock_shortcuts.GET.getlist.return_value = [0]
        
        res = challenge_page(mock_shortcuts)
        
        self.assertEqual(res, mock_redirect)
        mock_user.objects.get.assert_called_with(username='name')
        mock_notification.assert_called_with(user=mock_user, notification="name1 has invited you to a challenge # 0",
                                             link="/cipher/challengepage/?challenge_id=0", datetime='now')
        self.assertTrue(mock_notification.save.called)
        mock_redirect.assert_called_with('hi')
        
    @mock.patch('cccenter.views.context_processors')
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.challenge')
    @mock.patch('cccenter.views.comment')
    def test_challenge_page_Pass2(self, mock_comment, mock_challenge, mock_shortcuts, mock_user, mock_notify, mock_cp):
        mock_shortcuts.method = "GET"
        mock_shortcuts.GET.get.return_value = '0'
        mock_challenge.get_ciphertext.return_value = 'cipher'
        mock_challenge.user_in_challenge.return_value = (True, False)
        mock_challenge.get_challenge_info.return_value = {"challenge_type":"collaborative", "solved":True,
                                                          "users":['user1', 'user2'], "solved_by":['user1']}
        mock_challenge.get_difficulty.return_value = 'difficult'
        mock_shortcuts.user = mock_user
        mock_user.is_anonymous.return_value = False
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_comment.get_comments.return_value = 'comment'
        mock_cp.csrf.return_value = {'csrf':'hi'}
        mock_shortcuts.render.return_value = True
        
        res = challenge_page(mock_shortcuts)
        
        self.assertTrue(res)
        mock_challenge.get_ciphertext.assert_called_with(0)
        mock_challenge.user_in_challenge.assert_called_with(0, mock_user)
        mock_challenge.get_challenge_info.assert_called_with(0)
        mock_challenge.get_difficulty.assert_called_with(0)
        self.assertTrue(mock_user.is_anonymous.called)
        mock_notify.get_notifications.assert_called_with(mock_user, False)
        mock_notify.unviewed_notifications.assert_called_with(mock_user)
        mock_comment.get_comments.assert_called_with(0)
        mock_cp.csrf.assert_called_with(mock_shortcuts)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/challenge_page.html',
                                                 {"title":"Code and Cipher Center", "challenge_id":0,
                                                  "ciphertext":'cipher', "user_in_challenge":True, "difficulty":'difficult',
                                                  "challenge_type":'collaborative', "solved":True,
                                                  "num_users":2, "num_solved":1,
                                                  "users":['user1', 'user2'], "solved_by":['user1'], "solved_by_user":False,
                                                  "csrf":'hi', "notifications":'notify', "comments":"comment",
                                                  "unseen_notification":"unseen"})
            
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.Http404')
    def test_join_challenge_Pass1(self, mock_404, mock_shortcuts):
        mock_shortcuts.method = "GET"
        mock_404.return_value = mock_404
        
        res = join_challenge(mock_shortcuts)
        
        self.assertEqual(res, mock_404)
        
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.Http404')
    @mock.patch('cccenter.views.challenge')
    @mock.patch('cccenter.views.HttpResponseRedirect')
    def test_join_challenge_Pass2(self, mock_redirect, mock_challenge, mock_404, mock_shortcuts):
        mock_shortcuts.method = "POST"
        mock_shortcuts.POST.get.return_value = '0'
        mock_redirect.return_value = mock_redirect
        mock_shortcuts.user.id = 1
        
        res = join_challenge(mock_shortcuts)
        
        self.assertEqual(res, mock_redirect)
        mock_challenge.join_challenge.assert_called_with(challenge_id=0, user_id=1)
        mock_redirect.assert_called_with('/cipher/challengepage/?challenge_id=0')
        
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.context_processors')
    def test_login_Pass1(self, mock_cp, mock_shortcuts):
        mock_cp.csrf.return_value = {"csrf":'hi'}
        mock_shortcuts.render_to_response.return_value = True
        
        res = login(mock_shortcuts)
        
        self.assertTrue(res)
        mock_cp.csrf.assert_called_with(mock_shortcuts)
        mock_shortcuts.render_to_response.assert_called_with('cccenter/login.html',
                                                             {"active":"login",
                                                              "title":"Code and Cipher Center",
                                                              "csrf":'hi'})
                                                              
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.auth')
    @mock.patch('cccenter.views.HttpResponseRedirect')
    @mock.patch('cccenter.views.RequestContext')
    def test_auth_view_Pass1(self, mock_rc, mock_redirect, mock_auth, mock_shortcuts, mock_user):
        mock_shortcuts.POST.get.side_effect = auth_view_pass1_side_effect
        mock_auth.authenticate.return_value = mock_user
        mock_redirect.return_value = mock_redirect
        
        res = auth_view(mock_shortcuts)
        
        self.assertEqual(res, mock_redirect)
        mock_auth.authenticate.assert_called_with(username='name', password='pass')
        mock_auth.login.assert_called_with(mock_shortcuts, mock_user)
        mock_redirect.assert_called_with('/accounts/loggedin')
        
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.auth')
    @mock.patch('cccenter.views.RequestContext')
    def test_auth_view_Pass2(self, mock_rc, mock_auth, mock_shortcuts, mock_user):
        mock_shortcuts.POST.get.side_effect = auth_view_pass2_side_effect
        mock_auth.authenticate.return_value = None
        mock_rc.return_value = 'rc'
        mock_shortcuts.render_to_response.return_value = True
        
        res = auth_view(mock_shortcuts)
        
        self.assertTrue(res)
        mock_auth.authenticate.assert_called_with(username='name', password='pass')
        mock_rc.assert_called_with(mock_shortcuts, {"alert":"Invalid username or password!",
                                                    "title":"Code and Cipher Center"})
        mock_shortcuts.render_to_response.assert_called_with('cccenter/login.html', 'rc')
        
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.Q')
    @mock.patch('cccenter.views.Challenge')
    @mock.patch('cccenter.views.Cipher')
    @mock.patch('cccenter.views.notify')
    def test_challengeList_Pass1(self, mock_notify, mock_cipher, mock_challenge, mock_q, mock_shortcuts, mock_user):
        mock_shortcuts.user = mock_user
        mock_user.is_active = True
        mock_q.return_value = False
        mock_challenge.objects.filter.return_value = mock_challenge
        mock_challenge.distinct.return_value = [mock_cipher]
        mock_cipher.__iter__.return_value = mock_challenge
        mock_challenge.id = 0
        mock_challenge.objects.exclude.return_value = [mock_challenge]
        mock_cipher.objects.get.return_value = mock_cipher
        mock_cipher.difficulty = 'simple'
        mock_challenge.challenge_type = 'single'
        mock_shortcuts.user.is_anonymous.return_value = False
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_shortcuts.render.return_value = True
        mock_challenge.ciphertype = "cipher"
        mock_cipher.ciphertype = "cipher"
        
        res = challengeList(mock_shortcuts)
        
        self.assertTrue(res)
        mock_q.assert_called_with(users__in=[mock_user])
        mock_challenge.objects.filter.assert_called_with(False)
        self.assertTrue(mock_challenge.distinct.called)
        self.assertFalse(mock_challenge.objects.exclude.called)
        mock_cipher.objects.get.assert_called_with(ciphertype='cipher')
        self.assertTrue(mock_user.is_anonymous.called)
        mock_notify.get_notifications.assert_called_with(mock_user, False)
        mock_notify.unviewed_notifications.assert_called_with(mock_user)
        self.assertTrue(mock_shortcuts.render.called)
        
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.Challenge')
    @mock.patch('cccenter.views.Cipher')
    @mock.patch('cccenter.views.notify')
    def test_challengeList_Pass2(self, mock_notify, mock_cipher, mock_challenge, mock_shortcuts, mock_user):
        mock_shortcuts.user = mock_user
        mock_user.is_active = False
        mock_challenge.objects.filter.return_value = mock_challenge
        mock_challenge.distinct.return_value = [mock_cipher]
        mock_cipher.__iter__.return_value = mock_challenge
        mock_challenge.id = 0
        mock_challenge.objects.exclude.return_value = [mock_challenge]
        mock_cipher.objects.get.return_value = mock_cipher
        mock_cipher.difficulty = 'simple'
        mock_challenge.challenge_type = 'single'
        mock_shortcuts.user.is_anonymous.return_value = True
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_shortcuts.render.return_value = True
        mock_challenge.ciphertype = "cipher"
        mock_cipher.ciphertype = "cipher"
        
        res = challengeList(mock_shortcuts)
        
        self.assertTrue(res)
        self.assertFalse(mock_challenge.distinct.called)
        self.assertTrue(mock_challenge.objects.exclude.called)
        mock_cipher.objects.get.assert_called_with(ciphertype='cipher')
        self.assertTrue(mock_user.is_anonymous.called)
        self.assertFalse(mock_notify.get_notifications.called)
        self.assertFalse(mock_notify.unviewed_notifications.called)
        self.assertTrue(mock_shortcuts.render.called)
        
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.HttpResponseRedirect')
    def test_loggedin_Pass1(self, mock_redirect, mock_shortcuts):
        mock_redirect.return_value = mock_redirect
        
        res = loggedin(mock_shortcuts)
        
        mock_redirect.assert_called_with('/')
        
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.UserProfile')
    @mock.patch('cccenter.views.Challenge')
    @mock.patch('cccenter.views.Cipher')
    @mock.patch('cccenter.views.notify')
    def test_profile_Pass1(self, mock_notify, mock_cipher, mock_challenge, mock_userprofile, mock_user, mock_shortcuts):
        mock_user.objects.get.return_value = mock_user
        mock_user.userprofile = mock_userprofile
        mock_challenge.objects.filter.return_value = [mock_challenge]
        mock_cipher.objects.get.return_value = mock_cipher
        mock_cipher.difficulty = 'simple'
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_shortcuts.render.return_value = True
        mock_challenge.ciphertype = 'cipher'
        mock_cipher.difficulty = 'simple'
        mock_shortcuts.user = mock_user
        
        res = profile(mock_shortcuts)
        
        self.assertTrue(res)
        mock_user.objects.get.assert_called_with(username=mock_user)
        mock_challenge.objects.filter.assert_called_with(users=mock_user)
        mock_cipher.objects.get.assert_called_with(ciphertype='cipher')
        self.assertTrue(mock_shortcuts.render.called)
        
    @mock.patch('cccenter.views.shortcuts')
    def test_tutorial_Pass1(self, mock_shortcuts):
        mock_shortcuts.render.return_value = True
        
        res = tutorial(mock_shortcuts)
        
        self.assertTrue(res)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/tutorials.html',
                                                 {"title":"Code and Cipher Center",
                                                  "active":"tutorial"})
                                                  
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.notify')
    def test_notifications_Pass1(self, mock_notify, mock_user, mock_shortcuts):
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        mock_shortcuts.render.return_value = True
        mock_shortcuts.user = mock_user
        
        res = notifications(mock_shortcuts)
        
        self.assertTrue(res)
        mock_notify.get_notifications.assert_called_with(mock_user, True)
        mock_notify.unviewed_notifications(mock_user)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/notifications.html',
                                                 {"notifications":'notify',
                                                  "unseen_notification":'unseen',
                                                  "all_notifications":'notify'})
                                                  
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.UserProfile')
    @mock.patch('cccenter.views.User')
    @mock.patch('cccenter.views.SettingsForm')
    @mock.patch('cccenter.views.PasswordChangeForm')
    @mock.patch('cccenter.views.auth')
    @mock.patch('cccenter.views.HttpResponseRedirect')
    def test_settings_Pass1(self, mock_redirect, mock_auth, mock_pcf, mock_sf, mock_user, mock_userprofile, mock_shortcuts):
        mock_shortcuts.method = "POST"
        mock_shortcuts.user = mock_user
        mock_user.userprofile = mock_userprofile
        mock_sf.return_value = mock_sf
        mock_pcf.return_value = mock_pcf
        mock_pcf.is_valid.return_value = True
        mock_shortcuts.POST.get.side_effect = settings_pass1_side_effect
        mock_sf.is_valid.return_value = True
        mock_redirect.return_value = True
        mock_shortcuts.render.return_value = False
        mock_pcf.user = 'puser'
        
        res = settings(mock_shortcuts)
        
        self.assertTrue(res)
        self.assertTrue(mock_sf.called)
        self.assertTrue(mock_pcf.called)
        self.assertTrue(mock_pcf.save.called)
        mock_auth.update_session_auth_hash.assert_called_with(mock_shortcuts, 'puser')
        self.assertTrue(mock_user.save.called)
        self.assertTrue(mock_sf.is_valid.called)
        self.assertTrue(mock_sf.save.called)
        mock_redirect.assert_called_with('/profile/')
        
    @mock.patch('cccenter.views.notify')
    @mock.patch('cccenter.views.shortcuts')
    @mock.patch('cccenter.views.UserProfile')
    @mock.patch('cccenter.views.User')
    def test_settings_Pass2(self, mock_user, mock_userprofile, mock_shortcuts, mock_notify):
        mock_shortcuts.method = "GET"
        mock_shortcuts.user = mock_user
        mock_user.userprofile = mock_userprofile
        mock_shortcuts.render.return_value = True
        mock_notify.get_notifications.return_value = 'notify'
        mock_notify.unviewed_notifications.return_value = 'unseen'
        
        res = settings(mock_shortcuts)
        
        self.assertTrue(res)
        mock_notify.get_notifications.assert_called_with(mock_user, False)
        mock_notify.unviewed_notifications.assert_called_with(mock_user)
        mock_shortcuts.render.assert_called_with(mock_shortcuts, 'cccenter/settings.html',
                                                 {"title":"Code and Cipher Center",
                                                  "notifications":'notify',
                                                  "unseen_notification":'unseen'
                                                 })
