from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.shortcuts import resolve_url, redirect


class BaseProvider:
    CLIENT_ID_PARAMNAME = ''
    CLIENT_SECRET_PARAMNAME = ''

    REDIRECT_URI = ''
    LOGIN_URL = ''

    AUTH_URL = ''
    TOKEN_URL = ''
    SCOPE = None

    def __init__(self, request):
        self.request = request
        self.CLIENT_ID = getattr(settings, self.CLIENT_ID_PARAMNAME)
        self.CLIENT_SECRET = getattr(settings, self.CLIENT_SECRET_PARAMNAME)

        # Если указан state, то scope не нужен
        params = {
            'redirect_uri': self.get_redirect(),
            'state': self.get_state(),
        }
        if not params['state']:
            params['scope'] = self.SCOPE

        self.session = OAuth2Session(self.CLIENT_ID, **params)

    def get_redirect(self):
        return self.request.build_absolute_uri(resolve_url(self.REDIRECT_URI))

    def get_authorization_url(self):
        authorization_url, state = self.session.authorization_url(self.AUTH_URL)
        return authorization_url

    def get_state(self):
        return self.request.GET.get('state')

    def get_code(self):
        return self.request.GET.get('code')

    def get_data(self, token):
        pass

    def process_data(self, data):
        pass

    def get_login_url(self):
        if self.LOGIN_URL:
            return resolve_url(self.LOGIN_URL)

        referer = self.request.META.get('HTTP_REFERER')
        return referer or settings.LOGIN_URL

    @classmethod
    def redirect_view(cls, request):
        provider = cls(request)
        request.session['social_redirect'] = provider.get_login_url()
        return redirect(provider.get_authorization_url())

    @classmethod
    def info_view(cls, request):
        provider = cls(request)

        token = provider.session.fetch_token(
            provider.TOKEN_URL,
            client_secret=provider.CLIENT_SECRET,
            code=provider.get_code()
        )

        data = provider.get_data(token)
        provider.process_data(data)

        login_url = request.session.get('social_redirect', settings.LOGIN_URL)
        return redirect(login_url)


class GoogleProvider(BaseProvider):
    CLIENT_ID_PARAMNAME = 'GOOGLE_CLEINT_ID'
    CLIENT_SECRET_PARAMNAME = 'GOOGLE_CLIENT_SECRET'

    REDIRECT_URI = 'social:google-complete'

    SCOPE = ['email', 'profile']

    AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'

    def get_data(self, token):
        response = self.session.get('https://www.googleapis.com/oauth2/v1/userinfo')
        return response.json()

    def process_data(self, data):
        print(data)


class VKProvider(BaseProvider):
    CLIENT_ID_PARAMNAME = 'VK_CLEINT_ID'
    CLIENT_SECRET_PARAMNAME = 'VK_CLIENT_SECRET'

    REDIRECT_URI = 'social:vk-complete'

    AUTH_URL = 'https://oauth.vk.com/authorize'
    TOKEN_URL = 'https://oauth.vk.com/access_token'

    def get_data(self, token):
        url = ('https://api.vk.com/method/users.get?uids={user}&'
               'fields=uid,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo&'
               'access_token={token}')
        response = self.session.get(url.format(
            user=token.get('user_id'),
            token=token.get('access_token'),
        ))
        return response.json()

    def process_data(self, data):
        print(data)


class FacebookProvider(BaseProvider):
    CLIENT_ID_PARAMNAME = 'FACEBOOK_CLEINT_ID'
    CLIENT_SECRET_PARAMNAME = 'FACEBOOK_CLIENT_SECRET'

    REDIRECT_URI = 'social:facebook-complete'

    AUTH_URL = 'https://www.facebook.com/dialog/oauth'
    TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'

    def get_data(self, token):
        url = 'https://graph.facebook.com/me/?access_token={token}'
        response = self.session.get(url.format(
            token=token.get('access_token'),
        ))
        return response.json()

    def process_data(self, data):
        print(data)


PROVIDERS = {
    'google': GoogleProvider,
    'facebook': FacebookProvider,
    'vk': VKProvider,
}