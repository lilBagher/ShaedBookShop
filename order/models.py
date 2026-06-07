from django.db import models
from store.models import Book
from django.contrib.auth import get_user_model


class Order(models.Model):
    customer       = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='مشتری')
    name           = models.CharField(max_length=30, verbose_name='نام گیرنده')
    email          = models.EmailField(verbose_name='ایمیل')
    phone          = models.CharField(max_length=16, verbose_name='شماره تماس')
    address        = models.CharField(max_length=150, blank=True, null=True, verbose_name='آدرس')
    division       = models.CharField(max_length=20, blank=True, null=True, verbose_name='استان')
    district       = models.CharField(max_length=30, blank=True, null=True, verbose_name='شهر')
    zip_code       = models.CharField(max_length=30, blank=True, null=True, verbose_name='کد پستی')
    payment_method = models.CharField(max_length=20, blank=True, null=True, verbose_name='روش پرداخت')
    account_no     = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره حساب')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد تراکنش')
    payable        = models.IntegerField(verbose_name='مبلغ قابل پرداخت')
    totalbook      = models.IntegerField(verbose_name='تعداد کتاب')
    created        = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated        = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')
    paid           = models.BooleanField(default=False, verbose_name='پرداخت شده')

    class Meta:
        verbose_name        = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering            = ('-created',)

    def __str__(self):
        return f'سفارش شماره {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش')
    book     = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    price    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name        = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f'آیتم {self.id}'

    def get_cost(self):
        return self.price * self.quantity
