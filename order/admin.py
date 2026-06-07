from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    extra           = 0
    readonly_fields = ['book', 'price', 'quantity']
    can_delete      = False


class OrderAdmin(admin.ModelAdmin):
    # ✅ دقیقاً مثل نسخه اصلی — verbose_name مدل‌ها header رو فارسی می‌کنن
    list_display  = ['id', 'name', 'phone', 'email', 'paid', 'created', 'transaction_id']
    list_filter   = ['paid', 'created']
    search_fields = ['name', 'phone', 'email', 'transaction_id']
    readonly_fields = [
        'id', 'customer', 'payable', 'totalbook',
        'created', 'updated', 'transaction_id',
    ]
    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('id', 'customer', 'paid', 'transaction_id')
        }),
        ('اطلاعات گیرنده', {
            'fields': ('name', 'email', 'phone')
        }),
        ('مبلغ و زمان', {
            'fields': ('payable', 'totalbook', 'created', 'updated')
        }),
        ('اطلاعات تکمیلی', {
            'classes': ('collapse',),
            'fields': ('address', 'division', 'district', 'zip_code',
                       'payment_method', 'account_no'),
        }),
    )
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

admin.site.register(Order, OrderAdmin)
