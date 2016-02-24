import json
import tweepy
import urllib
import urllib2

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.generic.simple import redirect_to

from annoying.decorators import ajax_request
from annoying.decorators import render_to

from accounts.models import TwitterInfo, UserProfile
from accounts.models import DeliciousInfo
from accounts.renderers import connection_table_renderer

from api.models import MuteList
from api.models import Tag
from api.models import WhiteListItem


from common.view_helpers import _template_values, JSONResponse
from common.helpers import put_profile_pic
from common.admin import email_templates

from eyebrowse.log import logger
from eyebrowse.settings import TWITTER_CONSUMER_KEY
from eyebrowse.settings import TWITTER_CONSUMER_SECRET
from eyebrowse.settings import DELICIOUS_CONSUMER_KEY
from eyebrowse.settings import DELICIOUS_CONSUMER_SECRET
from notifications.models import Notification, NoticeType, send_now
from common.management.commands.update_popular_history import Command


@login_required
@render_to('accounts/whitelist.html')
def whitelist(request):
    """
        Edit whitelist entries
    """

    whitelist = WhiteListItem.objects.filter(user=request.user)

    return _template_values(request,
                            page_title="edit sharelist",
                            header="sharelist",
                            navbar='nav_account',
                            sub_navbar="subnav_whitelist",
                            whitelist=whitelist)


@login_required
@render_to('accounts/mutelist.html')
def mutelist(request):
    """
        Edit mutelist entries
    """

    mutelist = MuteList.objects.filter(user=request.user)

    return _template_values(request,
                            page_title="edit mute list",
                            header="mutelist",
                            navbar='nav_account',
                            sub_navbar="subnav_mutelist",
                            mutelist=mutelist)


@login_required
@render_to('accounts/account.html')
def account(request):
    """
        Edit account info
    """

    user = request.user

    if request.POST and request.is_ajax():
        success = False
        errors = {}
        data = None
        type = request.POST.get('form_type', None)

        if type == 'account-info':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            anon_email = request.POST.get('anon_checkbox', False) == 'True'
            location = request.POST.get('location', '')
            website = request.POST.get('website', '')
            bio = request.POST.get('bio', '')

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile = user.profile
            profile.anon_email = anon_email
            profile.location = location
            profile.website = website
            profile.bio = bio
            profile.save()

            success = "User info updated!"

        elif type == 'pic':
            pic_url = request.POST.get('pic_url')
            # download and upload to our S3
            pic_url = put_profile_pic(pic_url, user.profile)
            if pic_url:  # no errors/less than 1mb #patlsotw
                user.profile.pic_url = pic_url
                user.profile.save()
                success = "Profile picture changed!"
            else:
                errors['pic'] = ['Oops -- something went wrong.']

        resp = {
            'success': success,
            'errors': errors,
            'type': type,
            'data': data,
        }
        return JSONResponse(resp)

    return _template_values(request,
                            page_title="edit sharelist",
                            header="account info",
                            navbar='nav_account',
                            sub_navbar="subnav_account_info")


@login_required
@render_to('accounts/connections.html')
def connections(request):
    """
        Edit connection (following/followers)
    """

    following = request.user.profile.follows.all()
    followers = request.user.profile.followed_by.all()
    rendered_following = connection_table_renderer(
        following, 'following', following)
    rendered_followers = connection_table_renderer(
        followers, 'followers', following)

    template_dict = {
        "rendered_followers": rendered_followers,
        "rendered_following": rendered_following,
        "header": connections,
    }

    return _template_values(request,
                            page_title="edit connections",
                            navbar='nav_account',
                            sub_navbar="subnav_connections",
                            **template_dict)


@login_required
@render_to('accounts/sync_delicious.html')
def sync_delicious(request):
    """
        Edit connection (following/followers)
    """

    user = request.user

    template_dict = {"connected": False,
                     "synced": "You are not connected to Eyebrowse."}

    delicious_info = DeliciousInfo.objects.filter(user=user)
    if len(delicious_info) > 0:
        template_dict[
            "synced"] = "Your Delicious account is already connected to Eyebrowse."
        template_dict['connected'] = True
    else:
        if "code" in request.GET:
            code = request.GET.get("code")

            data = urllib.urlencode(
                {'client_id': DELICIOUS_CONSUMER_KEY,
                 'client_secret': DELICIOUS_CONSUMER_SECRET,
                 'grant_type': "code",
                 'redirect_uri': "http://eyebrowse.csail.mit.edu/accounts/profile/sync_delicious",
                 'code': code,
                 })

            results = json.loads(urllib2.urlopen(
                'https://avosapi.delicious.com/api/v1/oauth/token',
                data).read())

            access_token = results["access_token"]

            DeliciousInfo.objects.create(
                user=user, access_token=access_token)
            template_dict[
                "synced"] = "Your Delicious account is now connected to Eyebrowse!"
            template_dict['connected'] = True
        else:
            return redirect_to(request,
                               "https://delicious.com/auth/authorize?client_id=" +
                               DELICIOUS_CONSUMER_KEY +
                               "&redirect_uri=http://eyebrowse.csail.mit.edu/accounts/profile/sync_delicious")

    return _template_values(request,
                            page_title="Connect Delicious",
                            navbar='nav_account',
                            sub_navbar="subnav_sync_delicious",
                            **template_dict)


@login_required
@render_to('accounts/edit_tag.html')
def edit_tags(request):
    user = request.user
    tags = Tag.objects.filter(user=user)
    tag_dict = {}
    for tag in tags:
        if tag.name in tag_dict:
            tag_dict[tag.name].append(tag)
        else:
            tag_dict[tag.name] = [tag]

    template_dict = {"tags": tag_dict.values()}
    return _template_values(request,
                            page_title="Edit My Tags",
                            navbar='nav_account',
                            sub_navbar="subnav_edit_tags",
                            **template_dict)


def get_twitter_info(request, api, twit_obj, template_dict):
    template_dict['connected'] = True

    template_dict['username'] = twit_obj.twitter_username
    
    eye_friends = UserProfile.objects.get(user=request.user).follows.all().values_list('user__username', flat=True)
    
    friends = api.friends_ids()
    twitter_friends = TwitterInfo.objects.filter(twitter_id__in=friends)
    
    for friend in twitter_friends:
        friend.follows = str(friend.user.username in eye_friends)
    
    template_dict['twitter_friends'] = twitter_friends

@login_required
@render_to('accounts/sync_twitter.html')
def sync_twitter(request):
    """
        Edit connection (following/followers)
    """

    user = request.user

    template_dict = {"connected": False,
                     "synced": "You are not connected to Eyebrowse."}

    auth = tweepy.OAuthHandler(
        TWITTER_CONSUMER_KEY,
        TWITTER_CONSUMER_SECRET,
        "http://eyebrowse.csail.mit.edu/accounts/profile/sync_twitter")

    twitter_info = TwitterInfo.objects.filter(user=user)
    if len(twitter_info) > 0:
        auth.set_access_token(
            twitter_info[0].access_token,
            twitter_info[0].access_token_secret)

        api = tweepy.API(auth)
        template_dict[
            "synced"] = "Your Twitter account is already connected to Eyebrowse."
            
        get_twitter_info(request, api, twitter_info[0], template_dict)
            
    else:
        if "request_token" in request.session:
            token = request.session.pop("request_token")
            auth.request_token = token
            try:
                verifier = request.GET.get('oauth_verifier')
                auth.get_access_token(verifier)
                token = auth.access_token
                secret = auth.access_token_secret

                api = tweepy.API(auth)
                twitter_user = api.me()
                username = twitter_user.screen_name
                twitter_id = twitter_user.id

                twit_obj = TwitterInfo.objects.create(
                    user=user, twitter_username=username, twitter_id=twitter_id,
                    access_token=token, access_token_secret=secret)
                template_dict[
                    "synced"] = "Your Twitter account is now connected to Eyebrowse!"
                    
                get_twitter_info(request, api, twit_obj, template_dict)

            except tweepy.TweepError, e:
                logger.info(e)
                logger.info("Error! Failed to get access token")

        else:
            logger.info("no request_token")
            try:
                redirect_rule = auth.get_authorization_url()
                request.session["request_token"] = auth.request_token
                return redirect_to(request, redirect_rule)
            except tweepy.TweepError, e:
                logger.info(e)
                logger.info("Error! Failed to get request token")

    return _template_values(request,
                            page_title="Connect Twitter",
                            navbar='nav_account',
                            sub_navbar="subnav_sync_twitter",
                            **template_dict)


@login_required
@ajax_request
def connect(request):

    success = False
    errors = {}
    data = None
    req_prof = request.user.profile

    if request.POST and request.is_ajax():

        type = request.POST.get('type', None)
        username = request.POST.get('user', None)

        if type and username:
            user = User.objects.filter(username=username)
            if user.exists():
                user = user[0]
            else:
                user = None

            if not user:
                errors['user'] = "Requested user %s not found." % username

            elif user.profile == req_prof:
                errors['user'] = "Cannot follow yourself."

            else:
                if type == 'add-follow':
                    req_prof.follows.add(user.profile)
                    
                    try:
                        c = Command()
                        c.user_populate_history(request.user, user)
                    except Exception, e:
                        print e
                        
                    notice = NoticeType.objects.get(label="new_follower")
                    Notification.objects.create(recipient=user, sender=request.user, notice_type=notice)
                    send_now([user], "new_follower", sender=request.user)

                elif type == 'rm-follow' and req_prof.follows.filter(
                        user=user).exists():
                    req_prof.follows.remove(user)
                    
                    try:
                        c = Command()
                        c.remove_user_populate_history(request.user, user)
                    except Exception, e:
                        print e

            success = True
            data = {
                'type': type,
                'user': username,
            }

        else:
            errors[
                'user'] = 'Username required. Provided %s as username.' % username
            errors['type'] = 'Type required. Provided %s as type.' % type

    resp = {
        'success': success,
        'errors': errors,
        'data': data,
    }



    return resp
    