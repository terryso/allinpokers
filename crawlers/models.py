from django.db import models


class Player(models.Model):
    ori_id = models.CharField(u'会员Id', max_length=40, blank=True, unique=True)
    nick = models.CharField(u'昵称', max_length=50, db_index=True, blank=True)
    sex = models.IntegerField(u'性别', default=0)
    modify_nick_num = models.IntegerField(u'修改昵称次数', default=0)
    pool_rate = models.IntegerField(u'入池率', default=0)
    win_rate = models.IntegerField(u'胜率', default=0)
    hand_cnt = models.IntegerField(u'总手数', default=0)
    series_cnt = models.IntegerField(u'总局数', default=0)
    lose_number = models.IntegerField(u'输的手数', default=0)
    win_number = models.IntegerField(u'赢的手数', default=0)
    chip = models.IntegerField(u'筹码', default=0)
    cbet = models.IntegerField(u'持续下注', default=0)
    tanpai_rate = models.IntegerField(u'摊牌率', default=0)
    steal = models.IntegerField(u'偷盲率', default=0)
    per = models.IntegerField(u'翻牌前加注', default=0)
    total_earn = models.IntegerField(u'总盈利', default=0)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
