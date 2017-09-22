import os

import django
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView as BaseView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "allin_pokers.settings")
django.setup()

import requests
from crawlers.models import Player

def success_rsp(obj=None, http_rsp=False):
    if obj is not None:
        rsp_data = {'error_code': '0', 'error_message': '', u'result': obj}
    else:
        rsp_data = {'error_code': '0', 'error_message': ''}

    # log.debug(rsp_data)

    if http_rsp:
        return HttpResponse(JSONRenderer().render(rsp_data), content_type='application/json')
    else:
        return Response(rsp_data)


def error_rsp(code, msg, data=None, http_rsp=False):
    if data:
        rsp_data = {'error_code': code, 'error_message': msg, 'error_data': data}
    else:
        rsp_data = {'error_code': code, 'error_message': msg}
    if http_rsp:
        return HttpResponse(JSONRenderer().render(rsp_data), content_type='application/json')
    return Response(rsp_data)


class APIView(BaseView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def request_core_api(self, shop):
        pass


class ViewSet(ViewSetMixin, APIView):
    pass


def basic_info_crawler():
    try:
        for i in range(197871, 300000):
            user_id = str(i)
            user = get_user_info(user_id)
            if user is None:
                continue
            Player.objects.update_or_create(defaults=user, ori_id=user_id)
    except Exception as error:
        print(error)


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
    print(user_main)
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


def main():
    basic_info_crawler()


if __name__ == '__main__':
    main()
