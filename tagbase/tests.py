"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from django.db import models

from tagbase.models import *

class TaggerTest(object):
    """
>>> u, c = User.objects.get_or_create(username='uuu1', password='uuu1')
>>> u
<User: uuu1>

# init data
>>> i = Item.objects.create(user=u)
>>> i
<Item: 1:[]>

>>> ForbiddenTag.objects.create(name="aaa", user=u)
<ForbiddenTag: FB|aaa>

# test basic noun tagger
>>> from tagbase.utils import *
>>> n = NounTagger()
>>> n.tag(i, 'tag1', u)
<LiveTag: tag1>
>>> i
<Item: 1:[<LiveTag: tag1>]>
>>> i.tags.all()[0].tag
<Tag: NN|tag1>
>>> i.tags.all()[0].voters.all()
[]
>>> n.search(Item.objects.all(), ['tag1'])
[<Item: 1:[<LiveTag: tag1>]>]
>>> try:
...     n.tag(i, u'*', u)
... except ValueError as e:
...     print e
...
The NounTag could not be created because the data didn't validate.
>>> try:
...     n.tag(i, u'', u)
... except ValueError as e:
...     print e
...
The NounTag could not be created because the data didn't validate.


# test forbidden tag
>>> try:
...     n.tag(i, "aaa", u)
... except ForbiddenTagError as e:
...     print e.tag
...
aaa

# test basic like tagger
>>> l = LikeTagger('like')
>>> l0 = l.tag(i)
>>> l0
<LiveTag: like>
>>> l0.tag
<Tag: FN|like>
>>> i
<Item: 1:[<LiveTag: like>, <LiveTag: tag1>]>

# init data
>>> u1, c = User.objects.get_or_create(username='uuu1', password='uuu1')
>>> u2, c = User.objects.get_or_create(username='uuu2', password='uuu2')
>>> i2 = Item.objects.create(user=u1)
>>> i3 = Item.objects.create(user=u2)

# test general tagger
>>> g = GeneralTagger()
>>> l1 = g.like.tag(i2)
>>> l2 = g.noun.tag(i2, 'test', u1)
>>> l3 = g.noun.tag(i2, 'alpha', u2)
>>> l4 = g.like.tag(i3)
>>> l5 = g.noun.tag(i3, 'test', u1)
>>> l6 = g.noun.tag(i3, 'alpha', u1)

#  tag    vote
#--------------------------------
#   l0     u1
#   l1     u1, u2


>>> l0 = g.vote(l0.id, u1)
>>> l0.voters.all()
[<User: uuu1>]
>>> l0 = g.unvote(l0.id, u1)
>>> l0.voters.all()
[]
>>> l0 = g.vote(l0.id, u1)
>>> l1 = g.vote(l1.id, u1)
>>> l1.voters.all()
[<User: uuu1>]
>>> l1 = g.vote(l1.id, u2)
>>> l1.voters.all()
[<User: uuu1>, <User: uuu2>]
>>> l = g.vote(l4.id, u2)

>>> Item.objects.all()
[<Item: 1:[<LiveTag: like>, <LiveTag: tag1>]>, <Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like'])
[<Item: 1:[<LiveTag: like>, <LiveTag: tag1>]>, <Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['test'])
[<Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['alpha', 'test'])
[<Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]

# searching include function tag 'like' is not yet deployed,
# need to rewrite tests
>>> g.search(Item.objects.filter(), ['like', 'alpha', 'test'])
[<Item: 1:[<LiveTag: like>, <LiveTag: tag1>]>, <Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>, <Item: 3:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like'], u1)
[<Item: 1:[<LiveTag: tag1>, <LiveTag: like>]>, <Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]
>>> g.search(Item.objects.filter(), ['like', 'alpha'], u1)
[<Item: 2:[<LiveTag: like>, <LiveTag: test>, <LiveTag: alpha>]>]
    """