from django.conf import settings
from django.contrib.auth import authenticate, login, logout as logout_request
from django.contrib.auth.models import User
from django.http import JsonResponse

from repertory.api import _bad_request_method
from repertory.models import ReelUser
from repertory.utils.users import authorize_fb_token

def logout(request):
    logout_request(request)
    res = {'success': "You are logged out."}
    return JsonResponse(res, status=200)

def login_or_register(request):
    # Correct request method?
    if request.method != "POST":
        return _bad_request_method()
    # Got your token and ID?
    fb_access_token = "%s" % request.POST['fbAccessToken']
    fb_user_id = "%s" % request.POST['fbUserID']
    if not fb_access_token or not fb_user_id:
        res = {'error': "Missing request parameters."}
        return JsonResponse(res, status=400)
    fb_user = authorize_fb_token(fb_access_token, fb_user_id)
    if not fb_user:
        res = {'error': "Could not validate you with FB."}
        return JsonResponse(res, status=403)
    # Use long access token from now on
    fb_access_token = fb_user
    if request.user.is_authenticated():
        django_user = request.user
    else:
        # Do a user lookup
        new_user = False
        try:
            reeluser = ReelUser.objects.get(facebook_id=fb_user_id)
        except ReelUser.DoesNotExist:
            new_user = True
        else:
            if not reeluser.user:
                new_user = True
            else:
                django_user = reeluser.user
        if new_user:
            # You need a Django user account!
            django_pw = User.objects.make_random_password()
            django_user = User.objects.create_user(fb_user_id, password=django_pw)
            django_user.is_active = True
            django_user.save()
    # Maybe you're logged in, maybe you're not, but do you have a ReelUser?
    try:
        reeluser = django_user.reeluser
    except ReelUser.DoesNotExist:
        # Is there a ReelUser for your Facebook account?
        try:
            reeluser = ReelUser.objects.get(facebook_id=int(fb_user_id))
        except ReelUser.DoesNotExist:
            reeluser = ReelUser(facebook_id=int(fb_user_id), user=django_user)
            reeluser.save()
        else:
            # Is it associated with this user?
            if reeluser.user:
                if reeluser.user != django_user:
                    res = {'error': "User mismatch. Contact site admin."}
                    return JsonResponse(res, status=403)
    # OK, back to folks who aren't logged in
    if not request.user.is_authenticated():
        django_pw = User.objects.make_random_password()
        django_user.set_password(django_pw)
        django_user.save()
        user = authenticate(username=django_user.username, password=django_pw)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                res = {'error': "Your account is disabled. :("}
                return JsonResponse(res, status=403)
        else:
            res = {'error': "The system tried but failed to log you in."}
            return JsonResponse(res, status=500)
    # OK, back to everyone who's made it this far
    request.user.reeluser.fb_token = fb_access_token
    request.user.reeluser.save()
    res = {'success': "You're logged in.",
           'event_ids': list(request.user.reeluser.event_ids),
           'is_admin': request.user.reeluser.is_admin}
    return JsonResponse(res, status=200)