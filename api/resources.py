from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf.urls import url
from django.core.exceptions import MultipleObjectsReturned
from django.core.management import call_command

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from accounts.models import UserProfile
from api.models import *
from resource_helpers import *

from common.templatetags.filters import url_domain

class MyBasicAuthentication(BasicAuthentication):
    def __init__(self, *args, **kwargs):
        super(MyBasicAuthentication, self).__init__(*args, **kwargs)

    def is_authenticated(self, request, **kwargs):
        if 'sessionid' in request.COOKIES:
            s = Session.objects.filter(pk=request.COOKIES['sessionid'])
            if s.exists():
                s = s[0]
                if '_auth_user_id' in s.get_decoded():
                    u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                    request.user = u
                    return True 
        return False

class BaseMeta:
    """
        Abstract class to get basic authentication and authorization.
    """
    authentication = MyBasicAuthentication()
    authorization = DjangoAuthorization()
    serializer = urlencodeSerializer()

class BaseResource(ModelResource):
    """
        Subclass this to get generic ModelResource add-ins that TastyPie doesn't supply.
    """
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user) 

class UserResource(ModelResource):

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    class Meta(BaseMeta):
        queryset = User.objects.all()
        resource_name = 'user'
        
        detail_allowed_methods = ['get']
        list_allowed_methods = []
        fields = ['username', 'first_name', 'last_name', 'last_login']

        filtering = {
            'username': ALL,
        }

class UserProfileResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user')

    class Meta(BaseMeta):
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

        detail_allowed_methods = ['get']
        list_allowed_methods = []
        fields = ['pic_url']
        filtering = {
            'user' : ALL_WITH_RELATIONS
        }

class FilterSetItemResource(BaseResource):
    """
        Abstract base class
    """
    user = fields.ForeignKey(UserResource, 'user')  
    
    class Meta(BaseMeta):

        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'date_created': ALL,
            'url' : ALL,
        }
        resource_name = 'filterset'


class WhiteListItemResource(FilterSetItemResource):

    def obj_create(self, bundle, request=None, **kwargs):
        url = bundle.data['url']
        
        blacklist_item = get_BlackListItem(url) #check to see if this exists
        if blacklist_item:
            blacklist_item.delete()

        try:
            obj = WhiteListItem.objects.get(user=request.user, url=url)
        except WhiteListItem.DoesNotExist:
            return super(WhiteListItemResource, self).obj_create(bundle, request, user=request.user, **kwargs)
        except MultipleObjectsReturned: 
            #multiple items created, delete duplicates
            call_command("remove_duplicate_filtersets")
        return bundle

    class Meta(FilterSetItemResource.Meta):

        queryset = WhiteListItem.objects.select_related().all()
        resource_name = 'whitelist'

class BlackListItemResource(FilterSetItemResource):
    
    def obj_create(self, bundle, request=None, **kwargs):

        url = bundle.data['url']

        whitelist_item = get_WhiteListItem(url) #check to see if this exists
        if whitelist_item:
            whitelist_item.delete()
        try:
            obj = BlackListItem.objects.get(user=request.user, url=url)
        except BlackListItem.DoesNotExist:
            return super(BlackListItemResource, self).obj_create(bundle, request, user=request.user, **kwargs)        
        except MultipleObjectsReturned: 
            #multiple items created, delete duplicates
            call_command("remove_duplicate_filtersets")
        return bundle

    class Meta(FilterSetItemResource.Meta):

        queryset = BlackListItem.objects.select_related().all()
        resource_name = 'blacklist'


class EyeHistoryResource(BaseResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta(BaseMeta):
        queryset = EyeHistory.objects.select_related().all()
        resource_name = 'history-data'

        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'url' : ALL,
            'title' : ALL,
            'start_time' : ALL,
            'end_time' : ALL,
            'total_time' : ALL,
        }

    def obj_create(self, bundle, request=None, **kwargs):
        url = bundle.data['url']
        domain = url_domain(url)
        
        bundle.data["domain"] = domain

        title = bundle.data['title']
        total_time = bundle.data['total_time']
        src = bundle.data['src']
        
        if not in_Whitelist(url):
            return bundle
        try:
            obj = EyeHistory.objects.get(user=request.user, url=url, domain=domain, title=title, total_time=total_time, src=src)
        
        except EyeHistory.DoesNotExist:
            return super(EyeHistoryResource, self).obj_create(bundle, request, user=request.user, **kwargs)
        
        return bundle
