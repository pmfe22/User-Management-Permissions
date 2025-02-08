from django.urls import path
from .views import UserListView, UserDetailView , LoginView
from .views import user_panel , user_login , delete_user , edit_user , change_password_admin ,change_password_user, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path("login/", user_login, name="user-login"),
    path("panel/", user_panel, name="user-panel"),
    path("api/login/", TokenObtainPairView.as_view(), name="api-login"),
    path("delete-user/<int:user_id>/", delete_user, name="delete-user"),
    path("edit-user/<int:user_id>/", edit_user, name="edit-user"),
    path("change-password/admin/<int:user_id>/", change_password_admin, name="change-password-admin"),
    path("change-password/user/", change_password_user, name="change-password-user"),
    path("logout/", logout_view, name="logout"),

    #password recovery
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),        
]

