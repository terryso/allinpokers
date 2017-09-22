from rest_framework import serializers

from crawlers.models import Player


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('ori_id', 'nick', 'pool_rate', 'win_rate', 'hand_cnt', 'cbet', 'tanpai_rate', 'steal', 'per', 'total_earn')
