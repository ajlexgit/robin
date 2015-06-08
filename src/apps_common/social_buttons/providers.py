from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.shortcuts import resolve_url


class BaseProvider:
    CLIENT_ID_PARAMNAME = ''
    CLIENT_SECRET_PARAMNAME = ''

    PROVIDER_CODE = ''
    SCOPE = None

    def __init__(self, request):
        self.request = request
        self.CLIENT_ID = getattr(settings, self.CLIENT_ID_PARAMNAME)
        self.CLIENT_SECRET = getattr(settings, self.CLIENT_SECRET_PARAMNAME)

        params = {
            'redirect_uri': self.get_redirect(),
            'state': self.get_state(),
        }
        if not params['state']:
            params['scope'] = self.SCOPE

        self.session = OAuth2Session(self.CLIENT_ID, **params)

    def get_state(self):
        return self.request.GET.get('state')

    def get_code(self):
        return self.request.GET.get('code')

    def get_redirect(self,):
        return self.request.build_absolute_uri(resolve_url('social:complete')) + '?provider=' + self.PROVIDER_CODE


class GoogleProvider(BaseProvider):
    CLIENT_ID_PARAMNAME = 'GOOGLE_CLEINT_ID'
    CLIENT_SECRET_PARAMNAME = 'GOOGLE_CLIENT_SECRET'
    PROVIDER_CODE = 'google'
    SCOPE = ['email', 'profile']

    AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def get_authorization_url(self):
        authorization_url, state = self.session.authorization_url(self.AUTH_URL)
        return authorization_url

    def get_info(self):
        token = self.session.fetch_token(
            self.TOKEN_URL,
            client_secret=self.CLIENT_SECRET,
            code=self.get_code()
        )
        response = self.session.get(self.INFO_URL)
        return response.json()


PROVIDERS = {
    'google': GoogleProvider,
}