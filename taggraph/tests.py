from tagbase.models import *
from tagbase.utils import *
from taggraph.utils import *

class TextMinerTest(object):
    """
    # init data
>>> u = User.objects.create_user(username='uuu1', password='uuu1')
>>> n = NounTag.objects.create(name="test", sub_type='T', user=u)
>>> n = NounTag.objects.create(name="English", sub_type='T', user=u)
>>> n = NounTag.objects.create(name=u'\u7d10\u7d04\u5e02', sub_type='T', user=u)
>>> n = NounTag.objects.get_or_create(name=u'\u707d\u96e3', sub_type='T', user=u)

    # ASC-II test
>>> t = u'this is a simple test, and is for English only.'
>>> m = TextMiner(NounTag.objects.all())
>>> m.tags
frozenset([u'test', u'\u7d10\u7d04\u5e02', u'\u707d\u96e3', u'English'])
>>> m._tokenize(t)
[u'this', u'is', u'a', u'simple', u'test', u'and', u'is', u'for', u'English', u'only', u'']
>>> m.get_match_tags(t)
{u'test': 1, u'English': 1}

    # Unicode test
>>> t = u'\u4e94\u628a\u9470\u5319\u5728\u624b\uff0c\u6703\u8b93\u7d10\u7d04\u5e02\u9677\u5165\u707d\u96e3\uff0c'
>>> m.get_match_tags(t)
{u'\u7d10\u7d04\u5e02': 1, u'\u707d\u96e3': 1}
    """

class BaseTagGraphTest(object):
    """
# >>> g = BaseTagGraph()
# >>> g.graph = ALL_TAGS_GRAPH
# >>> g._pagerank()
    """

class TagGraphTest(object):
    """
>>> from tagbase.models import *
>>> init_data()
>>> tags = NounTag.objects.all()
>>> miner = TextMiner(tags)
>>> t = u"\u6fc3\u6fc3\u82f1\u570b\u53e3\u97f3\uff0c\u7559\u5e73\u982d\uff0c\u660e\u986f\u6709\u5728\u4e0a\u5065\u8eab\u623f\uff0c45\u6b72\u7684Jonathan Ive\u7a7f\u8457\u7121\u53ef\u6311\u5254\uff0c\u8b1b\u8a71\u65b9\u5f0f\u662f\u4e00\u5b57\u4e00\u53e5\u90fd\u7d93\u904e\u659f\u914c\uff0c\u5c0d\u65bc\u5de5\u4f5c\u6709\u4e0d\u53ef\u601d\u8b70\u7684\u71b1\u60c5\uff1b\u4ed6\u7684\u4e00\u4e9b\u540c\u4e8b\u8868\u793a\uff0c\u53ea\u8981\u4e00\u8ac7\u5230\u5de5\u4f5c\uff0cIve\u5c31\u5bb9\u5149\u7165\u767c\uff0c\u5728\u4ecb\u7d39\u4ed6\u500b\u4eba\u5c24\u5176\u559c\u6b61\u7684\u7522\u54c1\u7279\u8cea\uff0c\u6216\u8a0e\u8ad6\u89e3\u6c7a\u554f\u984c\u65b9\u6848\u6642\uff0c\u4ed6\u7e3d\u6703\u4e0d\u7531\u81ea\u4e3b\u9732\u51fa\u5145\u6eff\u611f\u67d3\u529b\u7684\u7b11\u5bb9\u3002\u4ed6\u662fApple\u7684\u5de5\u696d\u8a2d\u8a08\u8cc7\u6df1\u526f\u7e3d\u88c1\u2500\u2500Jonathan Ive\u2500\u2500\u7528\u8a2d\u8a08\u62c9\u8fd1\u4eba\u8207\u79d1\u6280\u9593\u7684\u8ddd\u96e2\uff0c\u8ca2\u737b\u6975\u5927\uff0c\u537b\u6975\u70ba\u8b19\u905c\u3002\u5f9e1998\u5e74Apple\u63a8\u51fa\u7684\u7cd6\u679c\u8272iMac\u5230\u4eca\u5e74\u7684iPad3\uff0c\u6bcf\u4ef6\u7522\u54c1\u7684\u66f2\u7dda\u3001\u958b\u95dc\u4ee5\u53ca\u5716\u793a\uff0c\u7121\u4e00\u4e0d\u662f\u5f62\u5851\u81ea\u8b1b\u8a71\u6eab\u99b4\u4f46\u8aaa\u670d\u529b\u5341\u8db3\u7684Jony\uff08\u670b\u53cb\u90fd\u9019\u9ebc\u53eb\u4ed6\uff09\u4e4b\u624b\u3002\u904e\u53bb12\u500b\u6708\u88e1\uff0cApple\u5df2\u6210\u70ba\u5168\u7403\u6700\u6709\u50f9\u503c\u516c\u53f8\uff0c\u7e3d\u5e02\u503c\u90543500\u5104\u82f1\u938a\u2500\u2500\u56e0\u70ba\u8a72\u516c\u53f8\u6709\u80fd\u529b\u5275\u9020\u51fa\u5168\u65b0\u7684\u7522\u54c1\uff0c\u66f4\u6709\u80fd\u529b\uff0c\u5efa\u7acb\u570d\u7e5e\u5728\u9019\u4e9b\u7522\u54c1\u56db\u5468\u7684\u7522\u696d\u751f\u614b\u93c8\u3002"
>>> from time import time
>>> start = time()
>>> g = TagGraph(miner)
>>> g.add_text(t)
>>> g.direct_tags
>>> g.related_tags
>>> time() - start
>>> g.export()
    """

def init_data():
    """
    Adding all terms to the database from the ALL_TAGS_GRAPH, mainly for testing usage.
    """
    u, created = User.objects.get_or_create(username='autorobo', password='autorobo')
    for n in ALL_TAGS_G.nodes_iter():
        if ALL_TAGS_G.out_degree(n) == 0:
            NounTag.objects.get_or_create(name=n, sub_type='H', user=u)
        else:
            NounTag.objects.get_or_create(name=n, sub_type='T', user=u)