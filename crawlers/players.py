import requests
from django.db.models import Q

from crawlers.models import Player
from crawlers.serializers import PlayerSerializer
from crawlers.views import success_rsp, ViewSet


from rq import Queue
from worker import conn

q = Queue(connection=conn)

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


def update_player_info(queryset):
    try:
        for user in queryset:
            user_id = user.ori_id
            user = get_user_info(user_id)
            if user is None:
                continue
            Player.objects.update_or_create(defaults=user, ori_id=user_id)
            print('更新玩家(%s)资料成功' % user.get('nick'))
    except Exception as error:
        print(error)

class PlayerViewSet(ViewSet):

    def list(self, request):
        query = request.GET.get('q', '')
        nick_names = query.split(',')

        conditions = None
        for i in range(0, len(nick_names)):
            nick_name = nick_names[i].strip()
            if i == 0:
                conditions = Q(nick__contains=nick_name)
            else:
                conditions = conditions | Q(nick__contains=nick_name)

        players = Player.objects.filter(conditions)
        ret = PlayerSerializer(players, many=True).data

        q.enqueue(update_player_info, players, timeout=600)

        return success_rsp(ret)
