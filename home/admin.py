from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from resources import PlayerResource, TeamResource
from .models import *
# Register your models here.


admin.site.register(CustomUserModel)
admin.site.register(ChoseTeamModel)

@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):
    resource_class = PlayerResource

@admin.register(TeamModel)
class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource