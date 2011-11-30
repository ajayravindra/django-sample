from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def fb_home(request):

    try:
        facebook_profile = request.user.get_profile().get_facebook_profile()
        facebook_friends = request.user.get_profile().get_facebook_friends()
    except:
        facebook_profile = facebook_friends = None

    if not facebook_profile or not facebook_friends:
        request.user.message_set.create(
            message="It looks like you're not using Facebook Connect.") 

    return render_to_response('index.html',
                              { 'facebook_profile': facebook_profile,
                                'facebook_friends': facebook_friends },
                              context_instance=RequestContext(request))
