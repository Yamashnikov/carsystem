from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from core.models import Customer, LoanScreeningInfo, CustomerCurrentVehicle
from members.models import CustomerAccount, GuestInvitation
from members.forms import (
    MemberLoginForm, PasswordChangeForm, GuestRegistrationForm, build_editable_once_form,
)
from members.auth import member_login_required, get_logged_in_customer


def login_view(request):
    if get_logged_in_customer(request):
        return redirect("members:mypage")

    form = MemberLoginForm(request.POST or None)
    error = None
    if request.method == "POST" and form.is_valid():
        member_id = form.cleaned_data["member_id"]
        password = form.cleaned_data["password"]
        customer = Customer.objects.filter(member_id=member_id, is_active=True).first()
        account = getattr(customer, "account", None) if customer else None

        if not customer or not account or not account.is_active:
            error = "会員IDまたはパスワードが正しくありません。"
        elif account.must_change_password and account.is_otp_expired:
            error = "ワンタイムパスワードの有効期限が切れています。管理者に再発行を依頼してください。"
        elif not account.check_password(password):
            error = "会員IDまたはパスワードが正しくありません。"
        else:
            request.session["customer_id"] = customer.pk
            account.last_login_at = timezone.now()
            account.save(update_fields=["last_login_at"])
            return redirect("members:mypage")

    return render(request, "members/login.html", {"form": form, "error": error})


def logout_view(request):
    request.session.flush()
    return redirect("members:login")


@member_login_required
def change_password_view(request):
    customer = request.customer
    account = customer.account
    form = PasswordChangeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        account.set_password(form.cleaned_data["new_password"])
        account.must_change_password = False
        account.otp_expires_at = None
        account.save()
        messages.success(request, "パスワードを変更しました。")
        return redirect("members:mypage")
    return render(request, "members/change_password.html", {"form": form, "customer": customer})


def _display_rows(instance, exclude=("id", "customer", "created_at", "updated_at")):
    """モデルインスタンスの現在値を、画面表示用の(ラベル, 値)リストに変換する"""
    rows = []
    for field in instance._meta.fields:
        if field.name in exclude:
            continue
        value = getattr(instance, field.name)
        if field.choices:
            display_method = getattr(instance, f"get_{field.name}_display", None)
            value = display_method() if display_method and value else value
        rows.append({"label": field.verbose_name, "value": value if value not in (None, "") else None})
    return rows


@member_login_required
def mypage_view(request):
    customer = request.customer
    screening, _ = LoanScreeningInfo.objects.get_or_create(customer=customer)
    current_vehicle, _ = CustomerCurrentVehicle.objects.get_or_create(customer=customer)

    CustomerForm = build_editable_once_form(Customer, customer)
    ScreeningForm = build_editable_once_form(LoanScreeningInfo, screening)
    VehicleForm = build_editable_once_form(CustomerCurrentVehicle, current_vehicle)

    customer_form = CustomerForm(instance=customer)
    screening_form = ScreeningForm(instance=screening)
    vehicle_form = VehicleForm(instance=current_vehicle)

    if request.method == "POST":
        which = request.POST.get("form_name")
        if which == "customer":
            customer_form = CustomerForm(request.POST, instance=customer)
            if customer_form.is_valid():
                customer_form.save()
                messages.success(request, "顧客情報を更新しました。")
                return redirect("members:mypage")
        elif which == "screening":
            screening_form = ScreeningForm(request.POST, instance=screening)
            if screening_form.is_valid():
                screening_form.save()
                messages.success(request, "ローン審査情報を更新しました。")
                return redirect("members:mypage")
        elif which == "vehicle":
            vehicle_form = VehicleForm(request.POST, instance=current_vehicle)
            if vehicle_form.is_valid():
                vehicle_form.save()
                messages.success(request, "現在使用中の車両情報を更新しました。")
                return redirect("members:mypage")

    context = {
        "customer": customer,
        "screening": screening,
        "current_vehicle": current_vehicle,
        "customer_form": customer_form,
        "screening_form": screening_form,
        "vehicle_form": vehicle_form,
        "customer_rows": _display_rows(customer, exclude=("id", "created_at", "updated_at", "is_active")),
        "screening_rows": _display_rows(screening),
        "vehicle_rows": _display_rows(current_vehicle),
    }
    return render(request, "members/mypage.html", context)


def guest_register_view(request, token):
    invitation = get_object_or_404(GuestInvitation, token=token)
    if invitation.used:
        return render(request, "members/guest_register_closed.html", {"reason": "このリンクは既に使用されています。"})

    form = GuestRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        from members.models import generate_member_id
        customer.member_id = generate_member_id()
        customer.save()

        account, raw_otp = CustomerAccount.issue_for_customer(customer)
        invitation.used = True
        invitation.created_customer = customer
        invitation.save()

        request.session["customer_id"] = customer.pk
        return render(request, "members/guest_register_done.html", {
            "customer": customer, "raw_otp": raw_otp,
        })

    return render(request, "members/guest_register.html", {"form": form})
