from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
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
    
    STATUS_CHOICES = [
        (PENDING, 'Đang chờ'),
        (COMPLETED, 'Hoàn thành'),
        (FAILED, 'Thất bại'),
    ]
    
    ZALOPAY = 'zalopay'
    MOMO = 'momo'
    VNPAY = 'vnpay'
    CASH = 'cash'
    
    METHOD_CHOICES = [
        (ZALOPAY, 'ZaloPay'),
        (MOMO, 'MoMo'),
        (VNPAY, 'VNPay'),
        (CASH, 'Tiền mặt'),
    ]
    
    bill_participant = models.ForeignKey(BillParticipant, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Số tiền'))
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=CASH, verbose_name=_('Phương thức'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING, verbose_name=_('Trạng thái'))
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (
            f"Payment: {self.bill_participant.user.username} "
            f"({self.bill_participant.bill.title}) - "
            f"Amount: {self.amount:,.2f} VND - "
            f"Method: {self.get_payment_method_display()} - "
            f"Status: {self.get_status_display()} - "
            f"Time: {self.payment_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
class Bill(models.Model):
    """
    Model cho hóa đơn cần chia
    """
    EQUAL = 'equal'
    CUSTOM = 'custom'
    PERCENTAGE = 'percentage'
    
    SPLIT_TYPE_CHOICES = [
        (EQUAL, 'Chia đều'),
        (CUSTOM, 'Tùy chỉnh'),
        (PERCENTAGE, 'Theo phần trăm'),
    ]
    
    CURRENCY_CHOICES = [
        ('VND', 'Vietnamese Dong'),
        ('USD', 'US Dollar'),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Tiêu đề'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Mô tả'))
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Tổng tiền')
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='VND',
        verbose_name=_('Loại tiền tệ')
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_bills'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='BillParticipant', 
        related_name='bills'
    )
    
    split_type = models.CharField(
        max_length=10, 
        choices=SPLIT_TYPE_CHOICES, 
        default=EQUAL, 
        verbose_name=_('Kiểu chia')
    )
    due_date = models.DateField(blank=True, null=True, verbose_name=_('Hạn thanh toán'))
    image = models.ImageField(upload_to='bills/%Y/%m/', blank=True, null=True, verbose_name=_('Hình ảnh hóa đơn'))
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Danh mục'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Ghi chú'))
    
    is_paid = models.BooleanField(default=False, verbose_name=_('Đã thanh toán'))
    is_archived = models.BooleanField(default=False, verbose_name=_('Đã lưu trữ'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.amount} {self.currency})"
    
    def get_total_paid(self):
        return sum(payment.amount for participant in self.billparticipant_set.all() 
                  for payment in participant.payments.filter(status=Payment.COMPLETED))

    def get_remaining_amount(self):
        return self.amount - self.get_total_paid()

class BillParticipant(models.Model):
    """
    Người tham gia chia hóa đơn
    """
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Số tiền phải trả')
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        null=True,
        blank=True,
        verbose_name=_('Phần trăm')
    )
    is_paid = models.BooleanField(default=False, verbose_name=_('Đã thanh toán'))
    reminder_sent = models.BooleanField(default=False, verbose_name=_('Đã gửi nhắc nhở'))
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('bill', 'user')
        indexes = [
            models.Index(fields=['is_paid']),
        ]
        
    def __str__(self):
        return f"{self.user.username} - {self.bill.title} ({self.amount} {self.bill.currency})"

    def get_paid_amount(self):
        return sum(payment.amount for payment in self.payments.filter(status=Payment.COMPLETED))

    def get_remaining_amount(self):
        return self.amount - self.get_paid_amount()

class Payment(models.Model):
    """
    Thanh toán cho hóa đơn
    """
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Đang chờ'),
        (COMPLETED, 'Hoàn thành'),
        (FAILED, 'Thất bại'),
        (REFUNDED, 'Đã hoàn tiền'),
        (CANCELLED, 'Đã hủy'),
    ]
    
    ZALOPAY = 'zalopay'
    MOMO = 'momo'
    VNPAY = 'vnpay'
    CASH = 'cash'
    BANK_TRANSFER = 'bank'
    CREDIT_CARD = 'credit'
    
    METHOD_CHOICES = [
        (ZALOPAY, 'ZaloPay'),
        (MOMO, 'MoMo'),
        (VNPAY, 'VNPay'),
        (CASH, 'Tiền mặt'),
        (BANK_TRANSFER, 'Chuyển khoản'),
        (CREDIT_CARD, 'Thẻ tín dụng'),
    ]
    
    bill_participant = models.ForeignKey(BillParticipant, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_('Số tiền')
    )
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=CASH, verbose_name=_('Phương thức'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING, verbose_name=_('Trạng thái'))
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    payment_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    
    payment_proof = models.ImageField(upload_to='payments/%Y/%m/', blank=True, null=True, verbose_name=_('Bằng chứng thanh toán'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Ghi chú'))
    
    class Meta:
        ordering = ['-payment_time']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['payment_time']),
        ]
    
    def __str__(self):
        return (
            f"Payment: {self.bill_participant.user.username} "
            f"({self.bill_participant.bill.title}) - "
            f"Amount: {self.amount:,.2f} {self.bill_participant.bill.currency} - "
            f"Method: {self.get_payment_method_display()} - "
            f"Status: {self.get_status_display()} - "
            f"Time: {self.payment_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
