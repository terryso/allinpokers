import requests
from django.contrib import admin
from rq import Queue

from worker import conn

q = Queue(connection=conn)

from crawlers.models import Player


def get_user_info(user_id):
    user_detail_url = 'http://cgi.allinpokers.com:8080/api/customer/detail?user_id=%s&operator_id=%s&room_type=0' % (
        user_id, user_id)
    detail_rsp = requests.get(user_detail_url)
    if detail_rsp.status_code != 200:
        print(detail_rsp.status_code)
        return None

    user_main_url = 'http://cgi.allinpokers.com:8080/api/data/person_main?user_id=%s' % user_id
    main_rsp = requests.get(user_main_url)
    if main_rsp.status_code != 200:
        return None

    user_detail = detail_rsp.json()
    user_main = main_rsp.json()
    # print(user_detail)
    # print(user_main)
    user = {
        'ori_id': user_id,
        'nick': user_detail.get('nick'),
        'chip': user_detail.get('chip'),
        'pool_rate': user_detail.get('pool_rate'),
        'win_rate': user_detail.get('win_rate'),
        'lose_number': user_detail.get('lose_number'),
        'win_number': user_detail.get('win_number'),
        'sex': user_detail.get('sex'),
        'modify_nick_num': user_detail.get('modify_nick_num'),
        'hand_cnt': user_main.get('hand_cnt'),
        'cbet': user_main.get('cbet'),
        'tanpai_rate': user_main.get('tanpai_rate'),
        'steal': user_main.get('steal'),
        'per': user_main.get('per'),
        'series_cnt': user_main.get('series_cnt'),
        'total_earn': user_main.get('total_earn'),
    }
    return user


def update_player_info_action(modeladmin, request, queryset):
    numbers = queryset.count()
    if numbers >= 10:
        q.enqueue(update_player_info, queryset, numbers, timeout=600)
    else:
        update_player_info(queryset, numbers)


def update_player_info(queryset, numbers):
    try:
        for user in queryset:
            user_id = user.ori_id
            user = get_user_info(user_id)
            if user is None:
                continue
            Player.objects.update_or_create(defaults=user, ori_id=user_id)
            print('更新玩家(%s)资料成功' % user.get('nick'))
        print('更新后%s名玩家资料成功' % numbers)
    except Exception as error:
        print(error)


def update_next_100_players_action(modeladmin, request, queryset):
    ori_id = int(queryset.first().ori_id)
    q.enqueue(update_next_players, ori_id, 100, timeout=600)


def update_next_1000_players_action(modeladmin, request, queryset):
    ori_id = int(queryset.first().ori_id)
    q.enqueue(update_next_players, ori_id, 1000, timeout=1800)


def update_next_players(ori_id, numbers):
    try:
        for i in range(ori_id, ori_id + numbers):
            user_id = str(i)
            user = get_user_info(user_id)
            if user is None:
                continue
            Player.objects.update_or_create(defaults=user, ori_id=user_id)
            print('更新玩家(%s)资料成功' % user.get('nick'))
        print('更新后%s名玩家资料成功' % numbers)
    except Exception as error:
        print(error)


def update_prev_100_players_action(modeladmin, request, queryset):
    ori_id = int(queryset.first().ori_id)
    q.enqueue(update_prev_players, ori_id, 100, timeout=600)


def update_prev_1000_players_action(modeladmin, request, queryset):
    ori_id = int(queryset.first().ori_id)
    q.enqueue(update_prev_players, ori_id, 1000, timeout=1800)


def update_prev_players(ori_id, numbers):
    try:
        for i in range(ori_id - numbers, ori_id):
            user_id = str(i)
            user = get_user_info(user_id)
            if user is None:
                continue
            Player.objects.update_or_create(defaults=user, ori_id=user_id)
            print('更新玩家(%s)资料成功' % user.get('nick'))
        print('更新前%s玩家资料成功' % numbers)
    except Exception as error:
        print(error)


update_player_info_action.short_description = "更新指定玩家资料"
update_next_100_players_action.short_description = "更新后100名玩家资料"
update_next_1000_players_action.short_description = "更新后1000名玩家资料"
update_prev_100_players_action.short_description = "更新前100名玩家资料"
update_prev_1000_players_action.short_description = "更新前1000名玩家资料"


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('ori_id', 'nick', 'total_earn', 'pool_rate', 'win_rate', 'hand_cnt', 'per')
    search_fields = ('ori_id', 'nick',)
    actions = [update_player_info_action, update_next_100_players_action, update_next_1000_players_action,
               update_prev_100_players_action, update_prev_1000_players_action]


admin.site.register(Player, PlayerAdmin)
