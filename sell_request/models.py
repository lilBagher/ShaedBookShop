from django.db import models
from django.contrib.auth.models import User


class BookSellRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار بررسی'),
        ('approved', 'تأیید شده'),
        ('rejected', 'رد شده'),
    ]

    CONDITION_CHOICES = [
        ('new', 'نو'),
        ('like_new', 'در حد نو'),
        ('good', 'خوب'),
        ('acceptable', 'قابل قبول'),
    ]

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sell_requests',
        verbose_name='فروشنده'
    )
    # category از اپ store
    category = models.ForeignKey(
        'store.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='دسته‌بندی'
    )
    name = models.CharField(max_length=100, verbose_name='نام کتاب')
    author_name = models.CharField(max_length=200, verbose_name='نام نویسنده')
    price = models.IntegerField(verbose_name='قیمت (تومان)')
    stock = models.IntegerField(default=1, verbose_name='تعداد موجودی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    coverpage = models.FileField(
        upload_to='sell_requests/covers/',
        verbose_name='تصویر جلد کتاب'
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='good',
        verbose_name='وضعیت کتاب'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت درخواست'
    )
    admin_note = models.TextField(
        blank=True,
        verbose_name='توضیحات ادمین'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')

    class Meta:
        verbose_name = 'درخواست فروش کتاب'
        verbose_name_plural = 'درخواست‌های فروش کتاب'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.seller.username} ({self.get_status_display()})"
