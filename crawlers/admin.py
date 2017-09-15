from django.contrib import admin

from crawlers.models import Player
from crawlers.views import get_user_info


def update_player_info(modeladmin, request, queryset):
    users = queryset.list()

    try:
        for user in users:
            user_id = user.ori_id
            user = get_user_info(user_id)
            if user is None:
                continue
            Player.objects.update_or_create(defaults=user, ori_id=user_id)
    except Exception as error:
        print(error)

update_player_info.short_description = "更新玩家资料"


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('ori_id', 'nick', 'sex', 'total_earn', 'pool_rate', 'win_rate', 'hand_cnt')
    search_fields = ('nick',)
    actions = [update_player_info]


admin.site.register(Player, PlayerAdmin)
