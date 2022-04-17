from email.policy import default
from django.conf import settings
from unicodedata import category
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField


# Create your models here.


class DiaryQuerySet(models.QuerySet):
    """
    予約投稿機能
    """

    def published(self):
        return self.filter(created_at__lte=timezone.now())


class Category(models.Model):
    """
    日記のカテゴリ
    """
    name = models.CharField('タイトル', max_length=255)

    def __str__(self) -> str:
        return self.name


class Diary(models.Model):
    """
    日記のモデル
    """
    title = models.CharField('タイトル', max_length=32)
    # thumbnail = models.ImageField('サムネイル')
    # 日記投稿はマークダウン対応
    text = MarkdownxField('本文')
    # on_deleteは紐づけられたオブジェクトも一緒に消すのかどうか、という設定をする
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    # updated_at = models.DateTimeField('更新日', default=timezone.now)

    objects = DiaryQuerySet.as_manager()

    def __str__(self) -> str:
        return self.title
