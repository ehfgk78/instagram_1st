from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from member.models import User
from post.models import Post, PostComment

admin.site.register(Post)
admin.site.register(PostComment)

admin.site.register(User, UserAdmin)