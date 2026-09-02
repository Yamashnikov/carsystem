from django.urls import path
from django.contrib.auth import views as auth_views
from staff import views

app_name = "staff"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="staff/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="staff:login"), name="logout"),
    path("", views.home_view, name="home"),
    path("customers/", views.customer_list_view, name="customer_list"),
    path("customers/new/", views.customer_create_view, name="customer_create"),
    path("customers/<int:pk>/", views.customer_detail_view, name="customer_detail"),
    path("customers/<int:pk>/issue-account/", views.issue_account_view, name="issue_account"),
    path("invitations/", views.invitation_list_view, name="invitation_list"),
]
