from django.contrib.auth.models import User
from django.db import models

from tagbase.models import NounTag

class Channel(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    name = models.SlugField(max_length=14, default="channel")
    tags = models.ManyToManyField(NounTag)

    def __unicode__(self):
        return u"%s:%s" % (self.user, self.tags.all())

    def to_json(self):
        j = {
            'id': self.id,
            'name': self.name,
            'tags': self.get_all_tags(),
        }
        return j

    def get_all_tags(self):
        return list(t.name for t in self.tags.all())

    def add_tag(self, tag_name):
        t = NounTag.objects.get(name=tag_name)
        self.tags.add(t)

    def remove_tag(self, tag_name):
        t = NounTag.objects.get(name=tag_name)
        self.tags.remove(t)