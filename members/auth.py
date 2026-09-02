from functools import wraps
from django.shortcuts import redirect
from core.models import Customer


def get_logged_in_customer(request):
    """セッションからログイン中の顧客を取得。未ログインならNone"""
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return None
    return Customer.objects.filter(pk=customer_id, is_active=True).first()


def member_login_required(view_func):
    """会員ページ用のログイン必須デコレータ（Djangoのadmin用authとは別系統）"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        customer = get_logged_in_customer(request)
        if not customer:
            return redirect("members:login")
        request.customer = customer
        account = getattr(customer, "account", None)
        if account and account.must_change_password and request.resolver_match.url_name != "change_password":
            return redirect("members:change_password")
        return view_func(request, *args, **kwargs)
    return wrapper
