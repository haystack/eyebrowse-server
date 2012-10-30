from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from django.contrib.auth.models import User

from accounts.models import UserProfile
from api.models import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'username': ALL,
        }


class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'
        allowed_methods = ['get']
        fields = ['pic_url']
        filtering = {
            'user' : ALL_WITH_RELATIONS
        }

class WhiteListItemResource(ModelResource):
    user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')
    
    class Meta:

        authorization = Authorization()
        queryset = WhiteListItem.objects.all()
        resource_name = 'whitelist'

        list_allowed_methods = ['get', 'post', 'put', 'delete']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user_profile': ALL_WITH_RELATIONS,
            'date_created': ALL,
            'url' : ALL,
        }

        def obj_create(self, bundle, request=None, **kwargs):

            return super(WhiteListItemResource, self).obj_create(bundle, request, user_profile=user_profile, **kwargs)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)

class BlackListItemResource(ModelResource):
    user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')
    
    class Meta:

        # authorization = DjangoAuthorization()
        queryset = BlackListItem.objects.all()
        resource_name = 'blacklist'

        list_allowed_methods = ['get', 'post', 'put', 'delete']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user_profile': ALL_WITH_RELATIONS,
            'date_created': ALL,
            'url' : ALL,
        }

        def obj_create(self, bundle, request=None, **kwargs):
            return super(WhiteListItemResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)

class EyeHistoryResource(ModelResource):
    user_profile = fields.ForeignKey(UserProfileResource, 'user_profile')

    class Meta:

        # authorization = DjangoAuthorization()
        queryset = EyeHistory.objects.all()
        resource_name = 'history-data'

        list_allowed_methods = ['get', 'put']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user_profile': ALL_WITH_RELATIONS,
            'url' : ALL,
            'title' : ALL,
            'start_time' : ALL,
            'end_time' : ALL,
            'total_time' : ALL,
        }

        def obj_create(self, bundle, request=None, **kwargs):
            return super(EyeHistoryResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user=request.user)