
from django.shortcuts import render, get_object_or_404


from project.settings import BANNED_GROUP, CLIENT_GROUP, MOD_GROUP, ACTIVE_USER, BANNED_USER
from decorators.decorators import admin_only, moderator_required

# Create your views here.

@moderator_required
def moderation_view(request):
    ctx={}

    template = 'apps/moderation/moderation.html'
    return render(request, template, ctx)
