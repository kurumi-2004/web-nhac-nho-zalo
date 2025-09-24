from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Mở rộng model User mặc định của Django
    """
    ZALO = 'zalo'
    FACEBOOK = 'facebook'
    EMAIL = 'email'
    
    AUTH_CHOICES = [
        (ZALO, 'Zalo'),
        (FACEBOOK, 'Facebook'),
        (EMAIL, 'Email'),
    ]
    
    auth_provider = models.CharField(
        max_length=10,
        choices=AUTH_CHOICES,
        default=EMAIL,
        verbose_name=_('Phương thức đăng nhập')
    )
    zalo_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Thông tin gói dịch vụ
    FREE = 'free'
    PRO = 'pro'
    TEAM = 'team'
    
    PLAN_CHOICES = [
        (FREE, 'Free'),
        (PRO, 'Pro'),
        (TEAM, 'Team'),
    ]
    
    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default=FREE,
        verbose_name=_('Gói dịch vụ')
    )
    plan_expiry = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """
    Thông tin bổ sung cho người dùng
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    notification_preferences = models.JSONField(default=dict)
    default_payment_method = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Hồ sơ của {self.user.username}"
    # Additional user profile fields
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notification settings
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    # Payment related fields
    payment_history = models.JSONField(default=list)
    subscription_status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        
    def get_notification_settings(self):
        """Returns user's notification preferences"""
        return {
            'email': self.email_notifications,
            'push': self.push_notifications,
            **self.notification_preferences
        }
    
    def update_payment_history(self, payment_data):
        """Adds new payment record to history"""
        if not isinstance(self.payment_history, list):
            self.payment_history = []
        self.payment_history.append({
            'date': payment_data.get('date'),
            'amount': payment_data.get('amount'),
            'method': payment_data.get('method'),
            'status': payment_data.get('status')
        })
        self.save()
