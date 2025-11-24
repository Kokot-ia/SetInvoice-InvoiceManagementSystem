from django.urls import path
from .views import (
    CustomLoginView, RegisterView, ProfileView,
    VerifyEmailView, ResendOTPView, VerificationSuccessView, AccountLockedView,
    CustomPasswordResetView, CustomPasswordResetConfirmView
)
from .user_views import UserListView, UserCreateView, UserUpdateView, UserToggleStatusView, UserDeleteView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Email Verification
    path('verify-email/<int:user_id>/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-otp/<int:user_id>/', ResendOTPView.as_view(), name='resend_otp'),
    path('verification-success/', VerificationSuccessView.as_view(), name='verification_success'),
    path('account-locked/', AccountLockedView.as_view(), name='account_locked'),
    
    # User Management (Admin only)
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:user_id>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:user_id>/toggle-status/', UserToggleStatusView.as_view(), name='user_toggle_status'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='user_delete'),
    
    # Password Reset (Custom)
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('password-reset-confirm/<uuid:token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
