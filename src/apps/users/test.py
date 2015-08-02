from django.conf import settings
from django.shortcuts import resolve_url
from django.test import SimpleTestCase, override_settings
from .models import CustomUser


@override_settings(DEBUG=True)
class Test1(SimpleTestCase):

    def test_register(self):
        # Wrong form
        response = self.client.post(resolve_url('users:register'), {
            'username': 'fred',
            'email': 'pix666@ya.ru',
            'password1': 'secret',
            'password2': 'secret1',
        })
        self.assertRedirects(response, resolve_url('users:register'))
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(username='fred')

        # Right form
        response = self.client.post(resolve_url('users:register'), {
            'username': 'fred',
            'email': 'pix666@ya.ru',
            'password1': 'secret',
            'password2': 'secret',
        })
        self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))
        try:
            CustomUser.objects.get(username='fred')
        except CustomUser.DoesNotExist:
            self.fail('User "fred" not found')

        # Go to profile
        self.client.login(username='fred', password='secret')
        response = self.client.get(resolve_url('users:profile', 'fred'))
        self.assertContains(response, '<b>E-mail</b>: pix666@ya.ru</p>')

        # Clean
        try:
            CustomUser.objects.get(username='fred').delete()
        except CustomUser.DoesNotExist:
            pass

    def test_login(self):
        response = self.client.post(resolve_url('users:login'), {
            'username': 'john',
            'password': 'wayne',
        })
        self.assertRedirects(response, resolve_url(settings.LOGIN_REDIRECT_URL))

        # Go to profile
        response = self.client.get(resolve_url('users:profile', 'john'))
        self.assertContains(response, '<b>E-mail</b>: pix667@ya.ru</p>')

        # Clean
        try:
            CustomUser.objects.get(username='john').delete()
        except CustomUser.DoesNotExist:
            pass
