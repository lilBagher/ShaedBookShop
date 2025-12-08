# order/admin.py
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemList(admin.TabularInline):
	model = OrderItem
	extra = 0
	# آیتم‌های سفارش را در ادمین فقط خواندنی می‌کنیم
	readonly_fields = ['book', 'price', 'quantity']

class OrderList(admin.ModelAdmin):
	# ۱. ستون‌هایی که در لیست سفارشات نمایش داده می‌شوند
	# 'id' همان کد پیگیری کاربر است
	list_display = ['id', 'name', 'phone', 'email', 'paid', 'created', 'transaction_id']

	list_filter = ['paid', 'created']
	search_fields = ['id', 'name', 'phone', 'email', 'transaction_id']

	# ۲. فیلدها را در صفحه "جزئیات سفارش" دسته‌بندی می‌کنیم
	fieldsets = (
		('اطلاعات اصلی سفارش (کدها)', {
			'fields': ('id', 'customer', 'paid', 'transaction_id')
		}),
		('اطلاعات مشتری (گیرنده)', {
			'fields': ('name', 'email', 'phone')
		}),
		('اطلاعات مبلغ و زمان', {
			'fields': ('payable', 'totalbook', 'created', 'updated')
		}),
		# ۳. فیلدهای اضافی که دیگر استفاده نمی‌شوند را در یک بخش مخفی قرار می‌دهیم
		('فیلدهای حذف شده (اختیاری)', {
			'classes': ('collapse',), # این بخش به صورت پیش‌فرض بسته است
			'fields': ('address', 'division', 'district', 'zip_code', 'payment_method', 'account_no'),
		}),
	)

	# ۴. فیلدهایی که نباید از داخل پنل ادمین دستی ویرایش شوند
	readonly_fields = ['id', 'customer', 'payable', 'totalbook', 'created', 'updated', 'transaction_id']

	inlines = [OrderItemList]

	# ۵. جلوی "اضافه کردن" سفارش به صورت دستی از ادمین را می‌گیریم
	def has_add_permission(self, request):
		return False

# مدل Order را با تنظیمات جدید OrderList ثبت می‌کنیم
admin.site.register(Order, OrderList)