from django.contrib import admin
from .models import Profile, Post, PostLikes, Followers

class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'userid', 'bio', 'profile_img', 'location')

# Register your models here.
# admin.site.register(Profile)
admin.site.register(Profile, UserProfilesAdmin)
admin.site.register(Post)
admin.site.register(PostLikes)
admin.site.register(Followers)


