from django.contrib import admin, messages
from django.utils.html import format_html
from core import models as m


class LoanScreeningInfoInline(admin.StackedInline):
    model = m.LoanScreeningInfo
    can_delete = False
    extra = 0


class CustomerCurrentVehicleInline(admin.StackedInline):
    model = m.CustomerCurrentVehicle
    can_delete = False
    extra = 0


class CustomerIdVerificationInline(admin.StackedInline):
    model = m.CustomerIdVerification
    can_delete = False
    extra = 0


@admin.register(m.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["member_id", "full_name", "mobile_phone", "has_car", "is_active", "account_status"]
    search_fields = ["member_id", "last_name", "first_name", "last_name_kana", "first_name_kana", "mobile_phone"]
    list_filter = ["is_active", "gender", "has_car"]
    inlines = [LoanScreeningInfoInline, CustomerCurrentVehicleInline, CustomerIdVerificationInline]
    actions = ["issue_member_account"]

    @admin.display(description="会員アカウント")
    def account_status(self, obj):
        account = getattr(obj, "account", None)
        if not account:
            return "未発行"
        return "有効" if account.is_active else "無効"

    @admin.action(description="選択した顧客に会員ID・会員アカウントを発行する（パターン①）")
    def issue_member_account(self, request, queryset):
        from members.models import CustomerAccount, generate_member_id
        issued = []
        for customer in queryset:
            if not customer.member_id:
                customer.member_id = generate_member_id()
                customer.save(update_fields=["member_id"])
            account, raw_otp = CustomerAccount.issue_for_customer(customer)
            issued.append(f"{customer} → 会員ID:{customer.member_id} / 初回パスワード:{raw_otp}")
        message = format_html("<br>".join(issued))
        self.message_user(
            request,
            format_html("以下の内容を顧客へSMS等で伝達してください（本番ではSMS自動送信に置き換える想定）：<br>{}",
                        message),
            level=messages.SUCCESS,
        )


@admin.register(m.ContactLog)
class ContactLogAdmin(admin.ModelAdmin):
    list_display = ["customer", "contact_method", "logged_at", "created_by"]
    list_filter = ["contact_method"]
    search_fields = ["customer__last_name", "customer__first_name", "content"]


@admin.register(m.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "is_active"]
    search_fields = ["name", "phone_number"]


@admin.register(m.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "contact_person", "phone_number", "standard_transport_cost", "is_active"]
    search_fields = ["name"]


@admin.register(m.LoanCompanyMaster)
class LoanCompanyMasterAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "is_active"]
    search_fields = ["name"]


@admin.register(m.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "seller", "purchase_price", "purchase_date", "listed_to", "sold_price"]
    list_filter = ["purchase_date"]
    search_fields = ["vehicle_info", "customer__last_name", "seller__name"]
    autocomplete_fields = ["customer", "seller"]


@admin.register(m.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["id", "maker", "model_name", "supplier", "status", "location_status",
                     "purchase_price", "total_cost_display", "is_active"]
    list_filter = ["status", "location_status", "inspection_status", "maker"]
    search_fields = ["maker", "model_name", "chassis_number", "license_plate"]
    autocomplete_fields = ["supplier", "origin_purchase"]

    @admin.display(description="原価合計")
    def total_cost_display(self, obj):
        return f"¥{obj.total_cost:,}"


class LoanApplicationInline(admin.TabularInline):
    model = m.LoanApplication
    extra = 0


class InhouseLoanContractInline(admin.StackedInline):
    model = m.InhouseLoanContract
    extra = 0
    can_delete = False


@admin.register(m.Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "vehicle", "payment_type", "progress_status",
                     "sale_price", "contract_date", "delivery_date"]
    list_filter = ["progress_status", "payment_type"]
    search_fields = ["customer__last_name", "customer__first_name", "desired_spec"]
    autocomplete_fields = ["customer", "vehicle", "trade_in_purchase", "loan_company"]
    inlines = [LoanApplicationInline, InhouseLoanContractInline]


class InhouseLoanPaymentInline(admin.TabularInline):
    model = m.InhouseLoanPayment
    extra = 0
    readonly_fields = ["original_due_date", "original_amount_due"]


@admin.register(m.InhouseLoanContract)
class InhouseLoanContractAdmin(admin.ModelAdmin):
    list_display = ["sale", "type", "contract_amount", "installment_count",
                     "remaining_balance_display", "remaining_count_display", "completed_at"]
    list_filter = ["type"]
    inlines = [InhouseLoanPaymentInline]
    actions = ["generate_schedule"]

    @admin.display(description="残債")
    def remaining_balance_display(self, obj):
        return f"¥{obj.remaining_balance:,}"

    @admin.display(description="残り回数")
    def remaining_count_display(self, obj):
        return f"{obj.remaining_count}回"

    @admin.action(description="選択した契約の返済予定を全回分生成する")
    def generate_schedule(self, request, queryset):
        for contract in queryset:
            contract.generate_payment_schedule()
        self.message_user(request, "返済予定を生成しました。", level=messages.SUCCESS)


admin.site.site_header = "中古車販売管理システム（β版）"
admin.site.site_title = "中古車販売管理システム"
admin.site.index_title = "業務メニュー"
