from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf.urls import url
from django.core.exceptions import MultipleObjectsReturned
from django.core.management import call_command
from django.db.models import Q

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from api.defaults import DEFAULT_BLACKLIST
from accounts.models import UserProfile
from api.models import *
from resource_helpers import *
from defaults import DEFAULT_BLACKLIST
from eyebrowse.log import logger

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

        #do not create if it is a default blacklist url
        if url in DEFAULT_BLACKLIST:
            return bundle

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


class EyeHistoryMessageResource(ModelResource):
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(eyehistory__user=request.user) 
    
    class Meta(BaseMeta):
        queryset = EyeHistoryMessage.objects.all()
        resource_name = 'history-message'
        
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

class EyeHistoryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    message = fields.ToManyField(EyeHistoryMessageResource, 'eyehistorymessage_set', null=True, blank=True, full=True)

    class Meta(BaseMeta):
        queryset = EyeHistory.objects.select_related().all().order_by('-start_time')
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
        
    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.user.username
        return bundle


    def obj_create(self, bundle, request=None, **kwargs):

        url = bundle.data['url']
        domain = url_domain(url)
          
        bundle.data["domain"] = domain
  
        title = bundle.data['title']
        total_time = bundle.data['total_time']
        
        src = bundle.data['src']
        
        message = bundle.data.get('message')
        
        if message and message.strip() == '':
            message = None
            
        if message:
            bundle.data.pop('message', None)
          
        if not in_Whitelist(url):
            return bundle
              
        try:
            try:
                obj = EyeHistory.objects.get(user=request.user, url=url, domain=domain, title=title, total_time=total_time, src=src)
                if message:
                    eye_message, created = EyeHistoryMessage.objects.get_or_create(eyehistory=obj, message=message)
            except EyeHistory.DoesNotExist:
                bundle_res = super(EyeHistoryResource, self).obj_create(bundle, request, user=request.user, **kwargs)
                if message:
                    eye_message, created = EyeHistoryMessage.objects.get_or_create(eyehistory=bundle_res.obj, message=message)
                return bundle_res;
        except Exception, e:
            logger.exception(e)
  
        except MultipleObjectsReturned:
            #multiple items created, delete duplicates
            call_command("remove_duplicate_history")
         
        return bundle



class ChatMessageResource(ModelResource):
    from_user = fields.ForeignKey(UserResource, 'from_user')
    to_user = fields.ForeignKey(UserResource, 'to_user')
    
    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(from_user=request.user) | Q(to_user=request.user) ) 
    
    def dehydrate(self, bundle):
        bundle.data['from_user'] = bundle.obj.from_user.username
        bundle.data['to_user'] = bundle.obj.to_user.username
        
        message = bundle.obj
        if message.read == False:
            message.read = True
            message.save()
        return bundle

    class Meta(BaseMeta):
        queryset = ChatMessage.objects.select_related().all()
        resource_name = 'chatmessages'

        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        excludes = ['id']
        filtering = {
            'from_user': ALL_WITH_RELATIONS,
            'to_user': ALL_WITH_RELATIONS,
            'url' : ALL,
            'read' : ALL,
            'date' : ALL,
            'messages': ALL,
        }

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(ChatMessageResource, self).apply_filters(request, applicable_filters)
        
        user1 = request.GET.get('username1', None)
        user2 = request.GET.get('username2', None)
        if user1 and user2:
            qset = (Q(from_user__username=user1,to_user__username=user2) | Q(from_user__username=user2,to_user__username=user1))
            base_object_list = base_object_list.filter(qset).distinct()
        return base_object_list

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            
            bundle.data['date'] = datetime.datetime.strptime(bundle.data['date']['_d'], '%Y-%m-%dT%H:%M:%S.%fZ')
            bundle.data['read'] = bool(bundle.data['read'])

            val = super(ChatMessageResource, self).obj_create(bundle, request, **kwargs)
        except Exception, e:
            logger.exception(e)
        return val
    
