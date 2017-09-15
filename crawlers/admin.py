from django.contrib import admin

from crawlers.models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('ori_id', 'nick', 'sex', 'total_earn', 'pool_rate', 'win_rate')
    search_fields = ('nick',)


admin.site.register(Player, PlayerAdmin)
