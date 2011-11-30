import simplejson as json, urllib

from django.db import models
from django.contrib.auth.models import User

class FacebookProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150)

    def get_facebook_profile(self):
        url = 'https://graph.facebook.com/me?access_token=%s' %self.access_token
        print url
        fb_profile = json.load(urllib.urlopen(url))

        # check if user has dis-allowed our app from connecting to FB
        if 'error' in fb_profile:
            print "error getting FB connection"
            #self.facebook_id = None
            #self.access_token = None
            #self.save()
            return None
        else:
            return fb_profile

    def get_facebook_friends(self):
        url = 'https://graph.facebook.com/me/friends?access_token=%s' % self.access_token
        print url
        fb_friends = json.load(urllib.urlopen(url))
        if 'error' in fb_friends:
            print "error getting FB connection"
            #self.facebook_id = None
            #self.access_token = None
            #self.save()
            return None
        else:
            return fb_friends

