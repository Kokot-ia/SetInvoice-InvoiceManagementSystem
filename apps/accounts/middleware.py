"""
Rate Limiting and IP Blocking Middleware for Django
Protects against brute force attacks and excessive requests
"""
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
import hashlib


class RateLimitMiddleware:
    """
    Middleware to limit requests per IP address
    - Blocks IPs making too many requests
    - Configurable rate limits
    - Automatic unblocking after timeout
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Configuration
        self.RATE_LIMIT = 100  # requests per window
        self.RATE_WINDOW = 60  # seconds
        self.BLOCK_DURATION = 900  # 15 minutes in seconds
        self.STRICT_PATHS = [
            '/accounts/login/',
            '/accounts/register/',
            '/accounts/password-reset/',
        ]
        self.STRICT_LIMIT = 10  # Lower limit for sensitive paths
        
    def __call__(self, request):
        # Get client IP
        ip_address = self.get_client_ip(request)
        
        # Check if IP is blocked
        if self.is_ip_blocked(ip_address):
            return self.blocked_response(request)
        
        # Check rate limit
        if not self.check_rate_limit(request, ip_address):
            self.block_ip(ip_address)
            return self.blocked_response(request)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    
    def is_ip_blocked(self, ip_address):
        """Check if IP is currently blocked"""
        block_key = f'blocked_ip:{ip_address}'
        return cache.get(block_key, False)
    
    def block_ip(self, ip_address):
        """Block an IP address for BLOCK_DURATION"""
        block_key = f'blocked_ip:{ip_address}'
        cache.set(block_key, True, self.BLOCK_DURATION)
        
        # Log the block
        print(f"[SECURITY] IP {ip_address} has been blocked for {self.BLOCK_DURATION} seconds")
    
    def check_rate_limit(self, request, ip_address):
        """Check if request is within rate limit"""
        path = request.path
        
        # Determine rate limit based on path
        if any(path.startswith(strict_path) for strict_path in self.STRICT_PATHS):
            limit = self.STRICT_LIMIT
        else:
            limit = self.RATE_LIMIT
        
        # Create cache key
        cache_key = f'rate_limit:{ip_address}:{path}'
        
        # Get current count
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limit:
            return False
        
        # Increment count
        cache.set(cache_key, current_count + 1, self.RATE_WINDOW)
        return True
    
    def blocked_response(self, request):
        """Return response for blocked IPs"""
        context = {
            'block_duration': self.BLOCK_DURATION // 60,  # Convert to minutes
        }
        return HttpResponseForbidden(
            render(request, 'accounts/ip_blocked.html', context).content
        )


class SecurityHeadersMiddleware:
    """
    Add security headers to all responses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net;"
        )
        
        return response
