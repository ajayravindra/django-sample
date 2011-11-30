import urllib


from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required
def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('http://' + settings.LOCALHOST_ALIAS +'/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

@login_required
def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')
    fb_user = authenticate(token=code, request=request)

    if not fb_user:
        request.user.message_set.create(
            message="Did you just disallow us from connecting to FB?"
        )

    url = getattr(settings, "LOGIN_REDIRECT_URL", "/")
    resp = HttpResponseRedirect(url)

    return resp

