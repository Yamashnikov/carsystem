from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from core.models import Customer
from staff.forms import StaffCustomerCreateForm, StaffCustomerEditForm


@login_required
def home_view(request):
    return render(request, "staff/home.html", {
        "customer_count": Customer.objects.filter(is_active=True).count(),
    })


@login_required
def customer_list_view(request):
    query = request.GET.get("q", "").strip()
    customers = Customer.objects.filter(is_active=True).order_by("-created_at")
    if query:
        customers = customers.filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query) |
            Q(last_name_kana__icontains=query) | Q(first_name_kana__icontains=query) |
            Q(member_id__icontains=query) | Q(mobile_phone__icontains=query)
        )
    return render(request, "staff/customer_list.html", {"customers": customers, "query": query})


@login_required
def customer_create_view(request):
    form = StaffCustomerCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customer = form.save()
        messages.success(request, f"{customer.full_name} 様を登録しました。続けて会員IDを発行できます。")
        return redirect("staff:customer_detail", pk=customer.pk)
    return render(request, "staff/customer_create.html", {"form": form})


@login_required
def customer_detail_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = StaffCustomerEditForm(request.POST or None, instance=customer)
    if request.method == "POST" and "save_customer" in request.POST and form.is_valid():
        form.save()
        messages.success(request, "顧客情報を更新しました。")
        return redirect("staff:customer_detail", pk=customer.pk)

    account = getattr(customer, "account", None)
    return render(request, "staff/customer_detail.html", {
        "customer": customer, "form": form, "account": account,
    })


@login_required
def issue_account_view(request, pk):
    """会員ID・会員アカウントを発行する（顧客詳細画面のボタンから呼ばれる）"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        from members.models import CustomerAccount, generate_member_id
        if not customer.member_id:
            customer.member_id = generate_member_id()
            customer.save(update_fields=["member_id"])
        account, raw_otp = CustomerAccount.issue_for_customer(customer)
        messages.success(
            request,
            f"会員ID「{customer.member_id}」、初回パスワード「{raw_otp}」を発行しました。"
            "この内容をお客様へお伝えください（本番ではSMSで自動送信する想定です）。",
        )
    return redirect("staff:customer_detail", pk=customer.pk)


@login_required
def invitation_list_view(request):
    """ゲスト招待（顧客自身が入力する登録用リンク）の一覧・新規発行"""
    from members.models import GuestInvitation

    if request.method == "POST":
        invitation = GuestInvitation.issue()
        messages.success(
            request,
            f"新しい登録リンクを発行しました： /register/{invitation.token}/ "
            "（このURLをお客様にお伝えください。1回使用すると無効になります）",
        )
        return redirect("staff:invitation_list")

    invitations = GuestInvitation.objects.order_by("-issued_at")[:50]
    return render(request, "staff/invitation_list.html", {"invitations": invitations})
