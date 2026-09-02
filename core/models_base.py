from django.db import models


class TimeStampedModel(models.Model):
    """全テーブル共通：作成日時・更新日時を自動記録する"""
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """論理削除フラグ。物理削除はせず、これをFalseにするだけで無効化する"""
    is_active = models.BooleanField("有効フラグ", default=True)

    class Meta:
        abstract = True
