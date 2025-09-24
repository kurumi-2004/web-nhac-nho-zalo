from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class RoommateGroup(models.Model):
    """
    Nhóm bạn cùng phòng
    """
    name = models.CharField(max_length=100, verbose_name=_('Tên nhóm'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='RoommateMembership', related_name='roommate_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class RoommateMembership(models.Model):
    """
    Thành viên trong nhóm bạn cùng phòng
    """
    ADMIN = 'admin'
    MEMBER = 'member'
    
    ROLE_CHOICES = [
        (ADMIN, 'Quản trị viên'),
        (MEMBER, 'Thành viên'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(RoommateGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    split_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, verbose_name=_('Tỷ lệ chia'))
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'group')
        
    def __str__(self):
        return f"{self.user.username} - {self.group.name}"

class RecurringExpense(models.Model):
    """
    Chi phí định kỳ của nhóm
    """
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'
    
    FREQUENCY_CHOICES = [
        (MONTHLY, 'Hàng tháng'),
        (QUARTERLY, 'Hàng quý'),
        (YEARLY, 'Hàng năm'),
    ]
    
    group = models.ForeignKey(RoommateGroup, on_delete=models.CASCADE, related_name='recurring_expenses')
    title = models.CharField(max_length=100, verbose_name=_('Tiêu đề'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Số tiền'))
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default=MONTHLY)
    due_day = models.PositiveSmallIntegerField(verbose_name=_('Ngày đến hạn'), help_text=_('Ngày trong tháng'))
    is_active = models.BooleanField(default=True)
