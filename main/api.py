from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from taggit.models import Tag
from main.models import Clipping


class CustomAuthentication(BasicAuthentication):
    def __init__(self, *args, **kwargs):
        super(CustomAuthentication, self).__init__(*args, **kwargs)
 
    def is_authenticated(self, request, **kwargs):
        from django.contrib.sessions.models import Session
        if 'sessionid' in request.COOKIES:
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in s.get_decoded():
                u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                request.user = u
                return True
        return super(CustomAuthentication, self).is_authenticated(request, 
                                                                  **kwargs)

class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
 
    def delete_list(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password']


class ClippingResource(ModelResource):
    tags = fields.ListField()
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Clipping.objects.all()
        resource_name = 'clipping'
        authentication = CustomAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True


    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
            
        orm_filters = super(ClippingResource, self).build_filters(filters)

        if 'tag' in filters:
            orm_filters['tags__name__in'] = filters['tag'].split(',')
        return orm_filters
    
        
    def dehydrate_tags(self, bundle):
        return map(str, bundle.obj.tags.all())


    def save_m2m(self, bundle):
        tags = bundle.data.get('tags', [])
        bundle.obj.tags.set(*tags)
        return super(ClippingResource, self).save_m2m(bundle)

    def obj_create(self, bundle, **kwargs):
        return super(ClippingResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
