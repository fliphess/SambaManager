from django.contrib import admin
from samba_manager.models import ManageableGroup, ManageableShare, ManageableUser


class ManageableGroupAdmin(admin.ModelAdmin):
    model = ManageableGroup


class ManageableShareAdmin(admin.ModelAdmin):
    model = ManageableShare


class ManageableUserAdmin(admin.ModelAdmin):
    model = ManageableUser


admin.site.register(ManageableUser, ManageableUserAdmin)
admin.site.register(ManageableGroup, ManageableGroupAdmin)
admin.site.register(ManageableShare, ManageableShareAdmin)
