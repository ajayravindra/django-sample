import cgi, urllib, simplejson as json

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
from facebook.models import FacebookProfile

class FacebookBackend:
    def authenticate(self, token=None, request=None):
        """ Reads in a Facebook code and asks Facebook if it's valid and what user it points to. """
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri('http://'+ settings.LOCALHOST_ALIAS + '/facebook/authentication_callback'),
            'code': token,
        }

        # Get a legit access token
        target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
        response = cgi.parse_qs(target)
        if not response:
            return None

        access_token = response['access_token'][-1]

        # Read the user's profile information
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
        fb_profile = json.load(fb_profile)

        try:
            # Try and find existing user
            fb_user = FacebookProfile.objects.get(facebook_id=fb_profile['id'])

            # Update access_token
            fb_user.access_token = access_token
            fb_user.save()

        except FacebookProfile.DoesNotExist:
            # Create the FacebookProfile
            fb_user = FacebookProfile(user=request.user, facebook_id=fb_profile['id'], access_token=access_token)
            fb_user.save()

        return fb_user

    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    supports_object_permissions = False
    supports_anonymous_user = True
