from tagbase.models import *
from django.db import IntegrityError
from django.db.models import Q

AUTO_USERNAME = 'autorobo'
AUTO_USERPWD = 'autorobo'
LIKE_TAG_NAME = 'like'

class BaseTagger(object):
    def _tag(self, object, tag, user):
#        live_tag = LiveTag.objects.create(content_object=object, tag=tag, user=user)
        f = LiveTagForm({'tag': tag.id, 'user': user.id})
        t = f.save(commit=False)
        t.content_object = object
        t.save()
        return t

    def get_tag(self, name):
        return Tag.objects.get(name=name)


class FunctionTagger(BaseTagger):
    def __init__(self, tag_name):
        self.autouser, created = User.objects.get_or_create(username=AUTO_USERNAME, password=AUTO_USERPWD)
#        self.tag_obj, created = FunctionTag.objects.get_or_create(user=self.autouser, name=tag_name)
        try:
            self.tag_obj = FunctionTag.objects.get(name=tag_name)
        except FunctionTag.DoesNotExist:
            f = FunctionTagForm({'user': self.autouser.id, 'name': tag_name})
#            print f.errors.as_text()
            self.tag_obj = f.save()

    def tag(self, object):
        return self._tag(object, self.tag_obj, self.autouser)


class LikeTagger(FunctionTagger):
    def search(self, queryset, user):
        "Get all objects which the user vote 'like'"
        qs = queryset.filter(tags__tag=self.tag_obj, tags__voters=user)
        return qs


class PinTagger(FunctionTagger):
    pass


class TrendTagger(FunctionTagger):
    pass


class WordTagger(BaseTagger):
    def search(self, queryset, tag_names):
        pass


forbidden_tags = frozenset(t.name for t in ForbiddenTag.objects.all())
class NounTagger(WordTagger):
    def _get_or_create_tag(self, tag_name, user):
        try:
            t = NounTag.objects.get(name=tag_name)
        except NounTag.DoesNotExist:
            t = self._create_tag(tag_name, user)
        return t

    def _create_tag(self, tag_name, user):
        if tag_name in forbidden_tags:
            raise ForbiddenTagError(tag_name)
#        t = NounTag.objects.create(name=tag_name, user=user)
        f = NounTagForm({'name': tag_name, 'user': user.id})
        return f.save()

    def bulk_tag(self, object, tag_names, user):
        for t in tag_names:
            self.tag(object, t, user)

    def tag(self, object, tag_name, user):
        try:
            t = NounTag.objects.get(name=tag_name)
        except NounTag.DoesNotExist:
            t = self._create_tag(tag_name, user)
        live_tag = self._tag(object, t, user)
#        live_tag.voters.add(user)
        return live_tag

    def search(self, queryset, tag_names):
        "Compute an && query, get all objects tagged with given tags."
        for n in tag_names:
            queryset = queryset.filter(tags__tag__name=n)
        return queryset


class GeneralTagger(object):
    def __init__(self):
        self.like = LikeTagger(LIKE_TAG_NAME)
        self.noun = NounTagger()

    def search(self, queryset, tag_names, user=None):
        tag_names = set(tag_names)
        fun_names = [LIKE_TAG_NAME]
        fun_names = set(fun_names)
        if LIKE_TAG_NAME in tag_names and user:
            tag_names.remove(self.like.tag_obj.name)
            qs = self.like.search(queryset, user)
            if tag_names:
                # quere for 'like' & ('tt1' & 'tt2' & ...)
                qs = self.noun.search(qs, tag_names)
        else:
            tag_names -= fun_names
            qs = self.noun.search(queryset, tag_names)
        return qs

    def vote(self, live_tag_id, user):
        live_tag = LiveTag.objects.select_related().get(id=live_tag_id)
        live_tag.vote(user=user)
        return live_tag

    def unvote(self, live_tag_id, user):
        live_tag = LiveTag.objects.select_related().get(id=live_tag_id)
        live_tag.unvote(user=user)
        return live_tag


class ForbiddenTagError(Exception):
    def __init__(self, tag):
        self.tag = tag