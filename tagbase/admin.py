from django.contrib import admin

from tagbase.models import *

admin.site.register(FunctionTag)
admin.site.register(NounTag)
admin.site.register(VerbTag)

autorobo, success = User.objects.get_or_create(username='autorobo', password='autorobo')

def import_tags():
    HUB_FILE_PATH = 'tagbase/fixtures/wired_hubs.txt'
    TERMINAL_FILE_PATH = 'tagbase/fixtures/wired_terminals.txt'

    f = file(HUB_FILE_PATH, "r")
    lines = f.readlines()
    f.close()
    for s in lines:
        s = s.replace('\n', '')
        NounTag.objects.get_or_create(user=autorobo, name=s, sub_type='H')

    f = file(TERMINAL_FILE_PATH, "r")
    lines = f.readlines()
    f.close()
    for s in lines:
        s = s.replace('\n', '')
        NounTag.objects.get_or_create(user=autorobo, name=s, sub_type='T')
