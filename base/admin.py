from django.contrib import admin
from api.models import UserData
from base.models import Camera, Brand, Gear

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("groups", "user_permissions")

admin.site.register(UserData,ProfileAdmin)
admin.site.register(Camera)
admin.site.register(Brand)
admin.site.register(Gear)
