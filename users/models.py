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
        return self.user.username
