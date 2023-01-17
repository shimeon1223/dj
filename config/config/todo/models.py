import datetime
from django.db import models # 最初はこれだけ
# ユーザー認証
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.utils import timezone

# Create your models here.
class Todo(models.Model):
    title = models.CharField("タスク名", max_length=30)
    description = models.TextField("詳細", blank=True)
    deadline = models.DateField("締切")

    def __str__(self):
        return self.title

# ユーザーアカウントのモデルクラス
class Account(models.Model):

    # ユーザー認証のインスタンス(1vs1関係)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 追加フィールド
    last_name = models.CharField(max_length=100,blank=True)
    first_name = models.CharField(max_length=100,blank=True)
    account_image = models.ImageField(upload_to="profile_pics",blank=True)

    def __str__(self):
        return self.user.username

class Schedule(models.Model):
    """スケジュール"""
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)

    def __str__(self):
        return self.summary
