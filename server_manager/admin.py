from django.contrib import admin
from server_manager.models import ServerCommand


class ServerCommandAdmin(admin.ModelAdmin):
    model = ServerCommand


admin.site.register(ServerCommand, ServerCommandAdmin)
