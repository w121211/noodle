from tastypie import fields
from tastypie.resources import ModelResource
from tagbase.models import *


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser',]
        allowed_methods = ['get']


class TagResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'


class NounTagResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = NounTag.objects.all()
        resource_name = 'nountag'