from django.contrib import admin, messages
from django.utils.html import format_html
from members.models import CustomerAccount, GuestInvitation


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ["customer", "is_active", "must_change_password", "otp_expires_at", "last_login_at"]
    readonly_fields = ["password_hash"]


@admin.register(GuestInvitation)
class GuestInvitationAdmin(admin.ModelAdmin):
    list_display = ["token", "used", "issued_at", "created_customer", "invitation_url"]
    actions = ["issue_new_invitation"]

    @admin.display(description="登録用URL（開発用に表示。本番は顧客へ個別に案内する）")
    def invitation_url(self, obj):
        return format_html("/register/{}/", obj.token)

    @admin.action(description="新しいゲスト招待（使い捨てトークン）を1件発行する")
    def issue_new_invitation(self, request, queryset):
        invitation = GuestInvitation.issue()
        self.message_user(
            request,
            format_html("新しい招待を発行しました。登録用URL： /register/{}/", invitation.token),
            level=messages.SUCCESS,
        )
