from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf.urls import url

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from accounts.models import UserProfile
from api.models import *

class MyBasicAuthentication(BasicAuthentication):
    def __init__(self, *args, **kwargs):
        super(MyBasicAuthentication, self).__init__(*args, **kwargs)

    def is_authenticated(self, request, **kwargs):
        if 'sessionid' in request.COOKIES:
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in s.get_decoded():
                u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                request.user = u
                return True
        return False

class BaseMeta:
    authentication = MyBasicAuthentication()
    authorization = DjangoAuthorization()

    def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)

class UserResource(ModelResource):
    class Meta(BaseMeta):
        queryset = User.objects.all()
        resource_name = 'user'
        
        detail_allowed_methods = ['get']
        list_allowed_methods = []
        fields = ['username', 'first_name', 'last_name', 'last_login']

        filtering = {
            'username': ALL,
        }

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

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

class FilterSetItemResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user' )
    
    class Meta(BaseMeta):

        #list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'date_created': ALL,
            'url' : ALL,
        }

class WhiteListItemResource(FilterSetItemResource):
    
    class Meta(FilterSetItemResource.Meta):

        queryset = WhiteListItem.objects.all()
        resource_name = 'whitelist'

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)
class BlackListItemResource(FilterSetItemResource):

    
    class Meta(FilterSetItemResource.Meta):

        queryset = BlackListItem.objects.all()
        resource_name = 'blacklist'

class EyeHistoryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta(BaseMeta):
        queryset = EyeHistory.objects.all()
        resource_name = 'history-data'

        list_allowed_methods = ['get', 'put']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'url' : ALL,
            'title' : ALL,
            'start_time' : ALL,
            'end_time' : ALL,
            'total_time' : ALL,
        }