from django.urls import path

from auth_app import views

app_name = "auth"

urlpatterns = [
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("auth/profile/<str:username>/", views.ProfileView.as_view(),
         name="profile"),
    path("auth/profile/<str:username>/edit/",
         views.ProfileUpdateView.as_view(), name="profile_edit"),
    path("auth/profile/<str:username>/password/",
         views.PasswordChangeView.as_view(), name="password_change"),
    path("auth/users/", views.UserListView.as_view(), name="user_list"),
    path("auth/delete-account/", views.DeleteAccountView.as_view(),
         name="delete_account")
]