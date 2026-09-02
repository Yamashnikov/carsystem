import random
import string
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from core.models_base import TimeStampedModel
from core.models import Customer


def generate_member_id():
    """会員ID：西暦下2桁 + 通し連番3桁（年をまたいで継続、1000で一周） + ランダム3桁"""
    year2 = timezone.now().strftime("%y")
    counter, _ = MemberIdCounter.objects.get_or_create(pk=1)
    counter.value = (counter.value + 1) % 1000
    counter.save()
    seq3 = f"{counter.value:03d}"
    for _ in range(20):  # 衝突したら作り直す（保険）
        rand3 = f"{random.randint(0, 999):03d}"
        candidate = f"{year2}{seq3}{rand3}"
        if not Customer.objects.filter(member_id=candidate).exists():
            return candidate
    raise RuntimeError("会員IDの生成に失敗しました（衝突が多発）。ランダム桁の設計を見直してください。")


class MemberIdCounter(models.Model):
    """会員ID中央3桁の通し連番を保持するだけのテーブル（1行だけ使う）"""
    value = models.PositiveIntegerField(default=0)


def generate_otp_password(length=8):
    """ワンタイムパスワード用のランダム文字列を生成"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


class CustomerAccount(TimeStampedModel):
    """会員アカウント（顧客と1:1）。ログインは顧客.member_idを使う"""
    customer = models.OneToOneField(Customer, verbose_name="顧客", on_delete=models.PROTECT,
                                     related_name="account")
    password_hash = models.CharField("パスワード（ハッシュ）", max_length=255)
    must_change_password = models.BooleanField("初回パスワード変更が必要か", default=True)
    otp_expires_at = models.DateTimeField("ワンタイムパスワードの有効期限", null=True, blank=True)
    is_active = models.BooleanField("有効フラグ", default=True)
    last_login_at = models.DateTimeField("最終ログイン日時", null=True, blank=True)

    class Meta:
        verbose_name = "会員アカウント"
        verbose_name_plural = "会員アカウント"

    def __str__(self):
        return f"会員アカウント（{self.customer}）"

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    @property
    def is_otp_expired(self):
        if not self.otp_expires_at:
            return False
        return timezone.now() > self.otp_expires_at

    @classmethod
    def issue_for_customer(cls, customer, otp_valid_hours=24):
        """顧客に対して会員アカウントを新規発行し、ワンタイムパスワードを返す"""
        raw_otp = generate_otp_password()
        account, _ = cls.objects.get_or_create(customer=customer)
        account.set_password(raw_otp)
        account.must_change_password = True
        account.otp_expires_at = timezone.now() + timezone.timedelta(hours=otp_valid_hours)
        account.is_active = True
        account.save()
        return account, raw_otp


def _random_token():
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))


class GuestInvitation(TimeStampedModel):
    """ゲスト招待（顧客自身が新規登録する際の使い捨てトークン）"""
    token = models.CharField("トークン", max_length=64, unique=True, default=_random_token)
    used = models.BooleanField("使用済みフラグ", default=False)
    issued_at = models.DateTimeField("発行日時", default=timezone.now)
    created_customer = models.ForeignKey(Customer, verbose_name="このトークンで作成された顧客",
                                          on_delete=models.PROTECT, null=True, blank=True,
                                          related_name="guest_invitation")

    class Meta:
        verbose_name = "ゲスト招待"
        verbose_name_plural = "ゲスト招待"

    def __str__(self):
        return f"招待 {self.token}（{'使用済み' if self.used else '未使用'}）"

    @classmethod
    def issue(cls):
        token = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))
        return cls.objects.create(token=token)
