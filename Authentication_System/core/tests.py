from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class SignInViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.sign_in_url = reverse('sign_in')

    def test_sign_in_get(self):
        response = self.client.get(self.sign_in_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign-in.html')

    def test_sign_in_post_success(self):
        response = self.client.post(self.sign_in_url, {'username': 'user', 'password': 'password'})
        self.assertRedirects(response, reverse('success'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully sign in!')

    def test_sign_in_post_invalid_credentials(self):
        response = self.client.post(self.sign_in_url, {'username': 'user', 'password': 'password1'})
        self.assertRedirects(response, self.sign_in_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid credentials!')

    def test_sign_in_authenticated_user(self):
        self.client.login(username='user', password='password')
        response = self.client.get(self.sign_in_url)
        self.assertRedirects(response, reverse('success'))


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_up_url = reverse('sign_up')

    def test_sign_up_get(self):
        response = self.client.get(self.sign_up_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign-up.html')

    def test_sign_up_post_success(self):
        response = self.client.post(self.sign_up_url, {
            'usermail': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        })
        self.assertRedirects(response, reverse('sign_in'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully sign up!')

    def test_sign_up_existing_username(self):
        User.objects.create_user(username='existinguser', password='testpass123')
        response = self.client.post(self.sign_up_url, {
            'usermail': 'newuser@example.com',
            'username': 'existinguser',
            'password': 'newpass123'
        })
        self.assertRedirects(response, self.sign_up_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Choose different user name!')

    def test_sign_up_existing_email(self):
        User.objects.create_user(username='user1', email='existing@example.com', password='testpass123')
        response = self.client.post(self.sign_up_url, {
            'usermail': 'existing@example.com',
            'username': 'newuser',
            'password': 'newpass123'
        })
        self.assertRedirects(response, self.sign_up_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Email already exist!')

    def test_sign_up_short_password(self):
        response = self.client.post(self.sign_up_url, {
            'usermail': 'newuser@example.com',
            'username': 'newuser',
            'password': 'short'
        })
        self.assertRedirects(response, self.sign_up_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Password is not secure!')

    def test_sign_up_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.sign_up_url)
        self.assertRedirects(response, reverse('success'))



class SignOutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password')
        self.sign_out_url = reverse('sign_out')

    def test_sign_out(self):
        self.client.login(username='user', password='password')
        response = self.client.get(self.sign_out_url)
        self.assertRedirects(response, reverse('sign_in'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Successfully Sign-out!')
        self.assertFalse('_auth_user_id' in self.client.session)



class SuccessViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.success_url = reverse('success')

    def test_success_view(self):
        response = self.client.get(self.success_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')