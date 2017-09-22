from django.db.models import Q

from crawlers.models import Player
from crawlers.serializers import PlayerSerializer
from crawlers.views import success_rsp, ViewSet


class PlayerViewSet(ViewSet):
    def list(self, request):
        q = request.GET.get('q')
        nick_names = q.split(',')

        q = None
        for i in range(0, len(nick_names)):
            if i == 0:
               q = Q(nick__contains=nick_names[i])
            else:
                q = q | Q(nick__contains=nick_names[i])

        players = Player.objects.filter(q)
        ret = PlayerSerializer(players, many=True).data

        return success_rsp(ret)

