from django.conf.urls import patterns, include

from tastypie.api import Api

from tagbase.api import *

api = Api(api_name='v1')
api.register(UserResource())
api.register(TagResource())

urlpatterns = patterns('',
    (r'^api/', include(api.urls)),
)