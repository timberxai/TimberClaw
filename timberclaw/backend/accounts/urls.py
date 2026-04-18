from django.urls import path

from . import views

urlpatterns = [
    path("auth/csrf/", views.CsrfCookieView.as_view()),
    path("auth/login/", views.LoginView.as_view()),
    path("auth/logout/", views.LogoutView.as_view()),
    path("me/", views.MeView.as_view()),
    path("debug/owner-admin-ping/", views.OwnerAdminPingView.as_view()),
]
