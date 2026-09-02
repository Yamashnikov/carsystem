from django.urls import path
from members import views

app_name = "members"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("mypage/", views.mypage_view, name="mypage"),
]
