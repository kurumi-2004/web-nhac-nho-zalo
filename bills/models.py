from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.core.validators import MinValueValidator

class Bill(models.Model):
    """
    Model cho hóa đơn cần chia
    """
    EQUAL = 'equal'
    CUSTOM = 'custom'
    
    SPLIT_TYPE_CHOICES = [
        (EQUAL, 'Chia đều'),
        (CUSTOM, 'Tùy chỉnh'),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Tiêu đề'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Mô tả'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Tổng tiền'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_bills')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BillParticipant', related_name='bills')
    
    split_type = models.CharField(max_length=10, choices=SPLIT_TYPE_CHOICES, default=EQUAL, verbose_name=_('Kiểu chia'))
    due_date = models.DateField(blank=True, null=True, verbose_name=_('Hạn thanh toán'))
    image = models.ImageField(upload_to='bills/', blank=True, null=True, verbose_name=_('Hình ảnh hóa đơn'))
    
    is_paid = models.BooleanField(default=False, verbose_name=_('Đã thanh toán'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class BillParticipant(models.Model):
    """
    Người tham gia chia hóa đơn
    """
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Số tiền phải trả'))
    is_paid = models.BooleanField(default=False, verbose_name=_('Đã thanh toán'))
    
    class Meta:
        unique_together = ('bill', 'user')
        
    def __str__(self):
        return f"{self.user.username} - {self.bill.title}"

class Payment(models.Model):
    """
    Thanh toán cho hóa đơn
    """
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
