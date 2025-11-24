"""
Email and OTP utility functions for user verification and password reset
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random


def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


def send_verification_email(user, otp):
    """
    Send verification email with OTP to user
    
    Args:
        user: User instance
        otp: 6-digit OTP string
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = 'Verify Your Email - Set Invoice'
    
    # HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #05CB3A; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 30px; }}
            .otp-box {{ background-color: white; border: 2px dashed #05CB3A; padding: 20px; text-align: center; margin: 20px 0; }}
            .otp-code {{ font-size: 32px; font-weight: bold; color: #05CB3A; letter-spacing: 5px; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            .button {{ background-color: #05CB3A; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Set Invoice</h1>
                <p>Invoice Management System</p>
            </div>
            <div class="content">
                <h2>Welcome to Set Invoice!</h2>
                <p>Thank you for registering. Please verify your email address to complete your registration.</p>
                
                <div class="otp-box">
                    <p>Your verification code is:</p>
                    <div class="otp-code">{otp}</div>
                    <p style="color: #666; font-size: 14px;">This code will expire in 1 minute</p>
                </div>
                
                <p>If you didn't create an account with Set Invoice, please ignore this email.</p>
                
                <p><strong>Security Tips:</strong></p>
                <ul>
                    <li>Never share your OTP with anyone</li>
                    <li>Set Invoice will never ask for your password via email</li>
                    <li>If you suspect unauthorized access, contact support immediately</li>
                </ul>
            </div>
            <div class="footer">
                <p>© 2025 Set Invoice - Invoice Management System</p>
                <p>by <a href="https://systemset.co" style="color: #05CB3A;">Systemset Co</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
    Welcome to Set Invoice!
    
    Thank you for registering. Please verify your email address to complete your registration.
    
    Your verification code is: {otp}
    
    This code will expire in 1 minute.
    
    If you didn't create an account with Set Invoice, please ignore this email.
    
    Security Tips:
    - Never share your OTP with anyone
    - Set Invoice will never ask for your password via email
    - If you suspect unauthorized access, contact support immediately
    
    © 2025 Set Invoice - Invoice Management System
    by Systemset Co (https://systemset.co)
    """
    
    try:
        print(f"[EMAIL DEBUG] Attempting to send verification email to: {user.email}")
        print(f"[EMAIL DEBUG] From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"[EMAIL DEBUG] Backend: {settings.EMAIL_BACKEND}")
        print(f"[EMAIL DEBUG] Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        print(f"[EMAIL DEBUG] TLS: {settings.EMAIL_USE_TLS}")
        print(f"[EMAIL DEBUG] User: {settings.EMAIL_HOST_USER}")
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"[EMAIL DEBUG] ✅ Email sent successfully to {user.email}")
        return True
    except Exception as e:
        print(f"[EMAIL DEBUG] ❌ Error sending verification email: {e}")
        print(f"[EMAIL DEBUG] Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


def send_password_reset_email(user, reset_url):
    """
    Send password reset email with secure link
    
    Args:
        user: User instance
        reset_url: Full URL for password reset
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    subject = 'Reset Your Password - Set Invoice'
    
    # HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #05CB3A; color: white; padding: 20px; text-align: center; }}
            .content {{ background-color: #f9f9f9; padding: 30px; }}
            .button {{ background-color: #05CB3A; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            .warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Set Invoice</h1>
                <p>Invoice Management System</p>
            </div>
            <div class="content">
                <h2>Password Reset Request</h2>
                <p>We received a request to reset your password for your Set Invoice account.</p>
                
                <p>Click the button below to reset your password:</p>
                
                <a href="{reset_url}" class="button">Reset Password</a>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #05CB3A;">{reset_url}</p>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong>
                    <ul style="margin: 10px 0;">
                        <li>This link will expire in 1 hour</li>
                        <li>This link can only be used once</li>
                        <li>If you didn't request this, please ignore this email</li>
                    </ul>
                </div>
                
                <p><strong>Security Tips:</strong></p>
                <ul>
                    <li>Never share your password reset link with anyone</li>
                    <li>Always use a strong, unique password</li>
                    <li>Enable two-factor authentication when available</li>
                </ul>
            </div>
            <div class="footer">
                <p>© 2025 Set Invoice - Invoice Management System</p>
                <p>by <a href="https://systemset.co" style="color: #05CB3A;">Systemset Co</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
    Password Reset Request
    
    We received a request to reset your password for your Set Invoice account.
    
    Click the link below to reset your password:
    {reset_url}
    
    Important:
    - This link will expire in 1 hour
    - This link can only be used once
    - If you didn't request this, please ignore this email
    
    Security Tips:
    - Never share your password reset link with anyone
    - Always use a strong, unique password
    - Enable two-factor authentication when available
    
    © 2025 Set Invoice - Invoice Management System
    by Systemset Co (https://systemset.co)
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
