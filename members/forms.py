from django import forms
from core.models import Customer, LoanScreeningInfo


class MemberLoginForm(forms.Form):
    member_id = forms.CharField(label="会員ID", max_length=8)
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput)


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(label="新しいパスワード", widget=forms.PasswordInput, min_length=8)
    new_password_confirm = forms.CharField(label="新しいパスワード（確認）", widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password") != cleaned.get("new_password_confirm"):
            raise forms.ValidationError("新しいパスワードが一致しません。")
        return cleaned


class GuestRegistrationForm(forms.ModelForm):
    """パターン②：ゲスト招待経由で顧客自身が入力する、最初の登録フォーム"""
    class Meta:
        model = Customer
        fields = [
            "last_name", "first_name", "last_name_kana", "first_name_kana",
            "gender", "birth_date", "mobile_phone", "email",
            "postal_code", "prefecture", "address_line", "building_room",
        ]
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}


def build_editable_once_form(model_class, instance):
    """
    「未入力のフィールドだけ編集可、入力済みは編集不可」を実現する動的フォーム。
    LoanScreeningInfo / CustomerIdVerification のように
    CUSTOMER_EDITABLE_ONCE_FIELDS を持つモデル専用。
    """
    editable_fields = []
    for field_name in model_class.CUSTOMER_EDITABLE_ONCE_FIELDS:
        current_value = getattr(instance, field_name, None)
        if current_value in (None, "", 0):
            editable_fields.append(field_name)

    class DynamicForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = editable_fields

    return DynamicForm
