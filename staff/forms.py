from django import forms
from core.models import Customer


class StaffCustomerCreateForm(forms.ModelForm):
    """スタッフが最低限の情報だけ入力して顧客レコードを作るためのフォーム（パターン①）"""
    class Meta:
        model = Customer
        fields = [
            "last_name", "first_name", "last_name_kana", "first_name_kana",
            "gender", "birth_date", "mobile_phone", "email",
        ]
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}
        labels = {f: Customer._meta.get_field(f).verbose_name for f in fields}


class StaffCustomerEditForm(forms.ModelForm):
    """スタッフ用：顧客の全項目を編集できるフォーム（会員ページと違い制限なし）"""
    class Meta:
        model = Customer
        exclude = ["member_id", "created_at", "updated_at"]
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}
