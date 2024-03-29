from django.conf.urls import patterns, url

urlpatterns = patterns('stream.views',
#    url(r'^$', 'test'),
    url(r'^stream/$', 'stream'),
    url(r'^post/(?P<post_id>\d+)/$', 'view_post'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'view_thread'),
)

urlpatterns += patterns('stream.ajax',
    # actions of post
    url(r'^api/post/get/$', 'get_posts'),
    url(r'^api/post/create/$', 'create_post'),
#    url(r'^api/post/re/$', 'reply_post'),
    url(r'^api/post/push/$', 'push_post'),
    url(r'^api/post/tag/$', 'tag_post'),
    url(r'api/post/autotag/', 'autotag_post'),
    # actions of push
    url(r'^api/push/get/$', 'get_pushes'),
    # actions of tag
    url(r'^api/tag/vote/$', 'vote_livetag'),
    url(r'^api/tag/unvote/$', 'unvote_livetag'),
    # actions of thread
)