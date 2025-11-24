from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Users, LoginAttempt
from .otp_utils import send_verification_email, send_password_reset_email, get_client_ip
from django import forms


class CustomLoginView(LoginView):
    """Enhanced login view with rate limiting and account lockout"""
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        """Record failed login attempt and check for unverified email"""
        email = form.cleaned_data.get('username')  # username field contains email
        ip_address = get_client_ip(self.request)
        
        if email:
            # Check if user exists but email not verified
            try:
                user = Users.objects.get(email=email)
                if not user.email_verified:
                    messages.warning(
                        self.request,
                        'Your email is not verified. Please verify your email to login.'
                    )
                    return redirect('verify_email', user_id=user.user_id)
            except Users.DoesNotExist:
                pass
            
            LoginAttempt.record_attempt(email, ip_address, successful=False)
            
            # Check if account is locked
            if LoginAttempt.is_locked(email, ip_address):
                messages.error(
                    self.request,
                    'Too many failed login attempts. Your account has been temporarily locked for 15 minutes.'
                )
                return redirect('account_locked')
        
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """Check email verification and record successful login"""
        user = form.get_user()
        email = user.email
        ip_address = get_client_ip(self.request)
        
        # Check if account is locked
        if LoginAttempt.is_locked(email, ip_address):
            messages.error(
                self.request,
                'Too many failed login attempts. Your account has been temporarily locked for 15 minutes.'
            )
            return redirect('account_locked')
        
        # Check if email is verified
        if not user.email_verified:
            # Generate and send new OTP for existing unverified users
            otp = user.generate_verification_token()
            
            if send_verification_email(user, otp):
                messages.warning(
                    self.request,
                    f'Please verify your email address before logging in. We\'ve sent a new verification code to {user.email}.'
                )
            else:
                messages.warning(
                    self.request,
                    'Please verify your email address before logging in. If you didn\'t receive the code, use the resend button.'
                )
            
            return redirect('verify_email', user_id=user.user_id)
        
        # Record successful login and clear failed attempts
        LoginAttempt.record_attempt(email, ip_address, successful=True)
        LoginAttempt.clear_attempts(email, ip_address)
        
        return super().form_valid(form)


class RegisterView(CreateView):
    """Registration view with email verification"""
    model = Users
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    
    def form_valid(self, form):
        # Save user but don't log them in yet
        user = form.save(commit=False)
        user.email_verified = False  # Ensure email is not verified
        user.save()
        
        # Generate and send OTP
        otp = user.generate_verification_token()
        
        if send_verification_email(user, otp):
            messages.success(
                self.request,
                f'Registration successful! We\'ve sent a verification code to {user.email}. Please check your inbox.'
            )
        else:
            messages.warning(
                self.request,
                'Registration successful, but we couldn\'t send the verification email. Please contact support.'
            )
        
        # Redirect to verification page
        return redirect('verify_email', user_id=user.user_id)


class VerifyEmailView(TemplateView):
    """Email verification view with OTP"""
    template_name = 'accounts/verify_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        try:
            user = Users.objects.get(user_id=user_id)
            context['user_email'] = user.email
            context['user_id'] = user_id
        except Users.DoesNotExist:
            pass
        return context
    
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        otp = request.POST.get('otp', '').strip()
        
        try:
            user = Users.objects.get(user_id=user_id)
            
            if user.verify_otp(otp):
                messages.success(request, 'Email verified successfully! You can now log in.')
                return redirect('verification_success')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
                return self.get(request, *args, **kwargs)
        
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')


class ResendOTPView(TemplateView):
    """Resend OTP for email verification"""
    
    def post(self, request, user_id):
        try:
            user = Users.objects.get(user_id=user_id)
            
            if user.email_verified:
                messages.info(request, 'Your email is already verified.')
                return redirect('login')
            
            # Generate new OTP
            otp = user.generate_verification_token()
            
            if send_verification_email(user, otp):
                messages.success(request, f'New verification code sent to {user.email}')
            else:
                messages.error(request, 'Failed to send verification email. Please try again later.')
            
            return redirect('verify_email', user_id=user_id)
        
        except Users.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('login')


class VerificationSuccessView(TemplateView):
    """Success page after email verification"""
    template_name = 'accounts/verification_success.html'


class AccountLockedView(TemplateView):
    """Account locked page"""
    template_name = 'accounts/account_locked.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'accounts/profile.html'


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view with secure tokens"""
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        """Generate custom reset token and send email"""
        email = form.cleaned_data['email']
        
        try:
            user = Users.objects.get(email=email)
            
            # Generate reset token
            reset_token = user.generate_reset_token()
            
            # Build reset URL
            reset_url = self.request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'token': reset_token})
            )
            
            # Send email
            if send_password_reset_email(user, reset_url):
                messages.success(
                    self.request,
                    'Password reset link has been sent to your email.'
                )
            else:
                messages.error(
                    self.request,
                    'Failed to send password reset email. Please try again later.'
                )
        
        except Users.DoesNotExist:
            # Don't reveal that the email doesn't exist (security)
            messages.success(
                self.request,
                'If an account exists with that email, a password reset link has been sent.'
            )
        
        return redirect(self.success_url)


class CustomPasswordResetConfirmView(FormView):
    """Custom password reset confirmation view"""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.kwargs.get('token')
        context['token'] = token
        return context
    
    def post(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return self.get(request, *args, **kwargs)
        
        # Find user with this token
        try:
            user = Users.objects.get(reset_token=token)
            
            if user.verify_reset_token(token):
                # Set new password
                user.set_password(new_password)
                user.reset_token = None
                user.reset_token_created = None
                user.save()
                
                messages.success(request, 'Password reset successful! You can now log in with your new password.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'Invalid or expired reset link. Please request a new one.')
                return redirect('password_reset')
        
        except Users.DoesNotExist:
            messages.error(request, 'Invalid reset link.')
            return redirect('password_reset')
