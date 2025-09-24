from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Reminder(models.Model):
    """
    Model cho chức năng nhắc nhở
    """
    ONCE = 'once'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    
    FREQUENCY_CHOICES = [
        (ONCE, 'Một lần'),
        (DAILY, 'Hàng ngày'),
        (WEEKLY, 'Hàng tuần'),
        (MONTHLY, 'Hàng tháng'),
    ]
    
    ZALO = 'zalo'
    FACEBOOK = 'facebook'
    EMAIL = 'email'
    ALL = 'all'
    
    CHANNEL_CHOICES = [
        (ZALO, 'Zalo'),
        (FACEBOOK, 'Facebook'),
        (EMAIL, 'Email'),
        (ALL, 'Tất cả'),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Tiêu đề'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Mô tả'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_reminders')
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='received_reminders')
    
    reminder_time = models.DateTimeField(verbose_name=_('Thời gian nhắc'))
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default=ONCE, verbose_name=_('Tần suất'))
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES, default=ALL, verbose_name=_('Kênh gửi'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Đang hoạt động'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
class ReminderResponse(models.Model):
    """
    Phản hồi cho nhắc nhở
    """
    CONFIRMED = 'confirmed'
    DECLINED = 'declined'
    PENDING = 'pending'
    
    STATUS_CHOICES = [
        (CONFIRMED, 'Đã xác nhận'),
        (DECLINED, 'Từ chối'),
        (PENDING, 'Đang chờ'),
    ]
    
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    response_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('reminder', 'user')
        
    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()} - {self.reminder.title}"