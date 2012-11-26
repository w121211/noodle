from django.utils import simplejson

import networkx
from networkx.readwrite import json_graph

from taggraph.models import *
from taggraph.utils import BaseTagGraph

def import_graphs():
    g = networkx.read_edgelist('taggraph/fixtures/wired_text_hubpagerank.edgelist',
        create_using=networkx.DiGraph())
    tg = BaseTagGraph()
    tg.graph = g
    tg._pagerank()
    j = tg.to_json()
    AllTagsGraph.objects.create(graph=simplejson.dumps(j))