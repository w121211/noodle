import sys

from channel.models import Channel
from tagcanal.models import *
from tagcanal.utils import *
from stream.ajax import response, response_errors
from stream.decorators import ajax_view


def _get_channels(request):
    resp = {
        'alert': None,
        'channels': [],
        }
    qs = Channel.objects.filter(user=request.user)
    for channel in qs:
        resp['channels'].append(channel.to_json())
    return response(resp)

def _resp_tags(request, channel_id):
    resp = {
        'alert': None,
        'tags': [],
        }
    c = Channel.objects.get(id=channel_id)
    resp['tags'] = c.get_all_tags()
    return response(resp)

@ajax_view
def get_channels(request):
    return _get_channels(request)

@ajax_view(method='POST')
def add_channel(request):
    Channel.objects.create(user=request.user)
    return _get_channels(request)

@ajax_view(method='POST')
def remove_channel(request):
    Channel.objects.get(id=request.POST['channel']).delete()
    return _get_channels(request)

@ajax_view(method='POST')
def add_tag(request):
    "add a tag to a channel"
    try:
        cid = request.POST['channel']
        Channel.objects.get(id=cid).add_tag(request.POST['tag'])
        return _resp_tags(request, cid)
    except NounTag.DoesNotExist:
        return response_errors("tag '%s' is not exist, cannot be added" % request.POST['tag'])
    except Exception as e:
        return response_errors(str(e))

@ajax_view(method='POST')
def remove_tag(request):
    "remove a tag to a channel"
    cid = request.POST['channel']
    Channel.objects.get(id=request.POST['channel']).remove_tag(request.POST['tag'])
    return _resp_tags(request, cid)