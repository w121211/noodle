import sys

from django.core import serializers
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe

from tagbase.models import *
from tagbase.utils import *
from taggraph.utils import TagGraph
from taggraph.utils import TextMiner
from stream.models import *
from stream.decorators import ajax_view

POSTS_PER_PAGE = 5

_tagger = GeneralTagger()
_miner = TextMiner(NounTag.objects.all())


def _paginate(queryset, item_num, time=None):
    """
    Return qs which <= time, with number of items specified
    """
    if not time:
        return queryset.filter()[:item_num]
    else:
        return queryset.filter(time__lt=time)[:item_num]


def response_errors(error_str):
    return HttpResponseForbidden(mark_safe(error_str))


def response(resp_data):
    resp = simplejson.dumps(resp_data, separators=(',', ':'))
    return HttpResponse(resp, mimetype='application/json')


@ajax_view
def get_posts(request):
    try:
        resp = {
            'alert': None,
            'posts': [],
            }
        tags = request.GET.get('t', None)
        time = request.GET.get('d', None)

        qs = Post.objects.all()
        if tags: # return posts by given tags
            tags = tags.split('+')
            qs = _tagger.search(qs, tags, request.user)
            qs = _paginate(qs, POSTS_PER_PAGE, time)
        else: # return all posts
            qs = _paginate(qs, POSTS_PER_PAGE, time)

        for post in qs:
            resp['posts'].append(post.to_json(request.user))
        if len(resp['posts']) == 0:
            return response_errors('no matching posts or no more posts')
        return response(resp)
    except Exception as e:
        return response_errors(str(e))


@ajax_view(method='POST')
def autotag_post(request):
    """
    Take a post content as input, find matching tags and return.
    {domain}/api/post/autotag/
    """
    resp = {
        'alert': None,
        'tags': [],
        }

    # Validate post content
    f = PostForm(request.POST)
    if not f.is_valid():
        return response_errors(f.errors.as_text())
    post = f.save(commit=False)

    # get matching tags
    g = TagGraph(_miner)
    g.add_text(post.title)
    g.add_text(post.body)
    #    resp['tags'] = list(g.direct_tags)
    resp['tags'] = g.get_recommend_tags()

    return response(resp)

# TODO fix ajax redirect (302) error. (1) add ajaxRedirectResponse (2) using view div to display html
@ajax_view(method='POST')
def create_post(request):
    """
    Create a new post.
    {domain}/api/post/create/
    """
    resp = {
        'alert': None,
        }

    # Validate post content
    f = PostForm(request.POST)
    if not f.is_valid():
        return response_errors(f.errors.as_text())
    post = f.save(commit=False)
    post.user = request.user
    post.save()

    # add tags
    tags = request.POST.getlist('tags[]')
    _tagger.like.tag(post)
    _tagger.noun.bulk_tag(post, tags, request.user)

    return response(resp)

@ajax_view(method='POST')
def reply_post(request):
    """
    Deprecated method.

    Reply a post.
    {domain}/api/post/reply/
    """
    if (request.is_ajax()):
        if (request.method == 'POST'):
            data = simplejson.loads(request.body)
            p = Post()
            p.user = request.user
            p.reply_post_id = data['reply_post_id']
            p.thread = data['thread_id']
            p.title = data['title']
            p.body = data['body']
            p.save()
    return HttpResponse("OK")

@ajax_view(method='POST')
def push_post(request):
    """
    Create a push.
    {domain}/api/post/pu/
    """
    resp = {
        'alert': None,
        'pushes': [],
        }
    f = PushForm(request.POST)
    if not f.is_valid():
        return response_errors(f.errors.as_text())
    push = f.save(commit=False)
    push.user = request.user
    push.save()

    _tagger.like.tag(push)
    resp['pushes'] = push.post.get_pushes(request.user)
    return response(resp)

@ajax_view(method='POST')
def tag_post(request):
    """
    User tag a specified post.
    {domain}/api/tag/post/
    """
    resp = {
        'alert': None,
        'tags': [],
    }
    try:
        f = LivetagForm(request.POST)
        if not f.is_valid():
            return response_errors(f.errors.as_text())

        p = Post.objects.get(id=f.cleaned_data['item'])
        _tagger.noun.tag(p, f.cleaned_data['tag'], request.user)
        resp['tags'] = p.get_tags(request.user)
        return response(resp)
    except ForbiddenTagError as e:
#        resp['alert'] = "%s cannot be used as the tag" % e.tag
        response_errors("%s cannot be used as the tag" % e.tag)
    except Exception as e:
        response_errors(str(e))

@ajax_view
def vote_livetag(request):
    """
    User can vote a live tag (a tag of an object) with a given live tag id.
    {domain}/api/tag/vote/
    """
    resp = {
        'alert': None,
        'tags': [],
    }
    try:
        l = _tagger.vote(request.GET['t'], request.user)
        item = l.content_object
        resp['tags'] = item.get_tags(request.user)
    except LiveTag.DoesNotExist:
        resp['alert'] = "cannot find the live tag"
    except Exception as e:
        print e
    return response(resp)

@ajax_view
def unvote_livetag(request):
    """
    User can vote a live tag (a tag of an object) with a given live tag id.
    {domain}/api/tag/unvote/
    """
    resp = {
        'alert': None,
        'tags': [],
        }
    try:
        l = _tagger.unvote(request.GET['t'], request.user)
        item = l.content_object
        resp['tags'] = item.get_tags(request.user)
    except LiveTag.DoesNotExist:
        resp['alert'] = "cannot find the live tag"
    return response(resp)

def get_pushes(request):
    """
    Undecided function
    {domain}/json/push/get/
    """
    data = None
    if (request.is_ajax()):
        if (request.method == 'GET'):
            pushes = Push.objects.filter(post_id=request.GET['id'])
            if (pushes):
                data = list()
                for push in pushes:
                    data.append({
                        'user': push.user.__unicode__(),
                        'body': push.body,
                        })
                data = simplejson.dumps(data)
    if (data):
        return HttpResponse(data, mimetype='application/json')
    else:
        return HttpResponse('fail')