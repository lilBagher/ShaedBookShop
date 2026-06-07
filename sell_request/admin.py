from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from django.contrib import messages
from .models import BookSellRequest


def _create_unique_slug(name):
    from store.models import Book
    import uuid
    base_slug = slugify(name, allow_unicode=True) or str(uuid.uuid4())[:8]
    slug, counter = base_slug, 1
    while Book.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    return slug


def approve_and_publish(modeladmin, request, queryset):
    """تأیید درخواست‌ها و اضافه کردن خودکار به فروشگاه"""
    from store.models import Book, Writer
    approved_count = 0

    for sell_req in queryset.filter(status='pending'):
        try:
            writer = None
            if sell_req.author_name:
                writer_slug = slugify(sell_req.author_name, allow_unicode=True) or f'writer-{sell_req.pk}'
                writer = Writer.objects.filter(slug=writer_slug).first()
                if not writer:
                    writer = Writer.objects.create(
                        name=sell_req.author_name,
                        slug=writer_slug,
                        bio=f'کتاب‌فروش: {sell_req.seller.username}',
                        pic='',
                    )

            Book.objects.create(
                writer=writer,
                category=sell_req.category,
                name=sell_req.name,
                slug=_create_unique_slug(sell_req.name),
                price=sell_req.price,
                stock=sell_req.stock,
                coverpage=sell_req.coverpage,
                bookpage='',
                description=sell_req.description,
                status=0,
            )
            sell_req.status = 'approved'
            sell_req.save()
            approved_count += 1

        except Exception as e:
            modeladmin.message_user(
                request,
                f'خطا در ثبت کتاب «{sell_req.name}»: {e}',
                level=messages.ERROR
            )

    if approved_count:
        modeladmin.message_user(
            request,
            f'✅ {approved_count} کتاب تأیید و به فروشگاه اضافه شد.',
            level=messages.SUCCESS
        )


approve_and_publish.short_description = '✅ تأیید و انتشار در فروشگاه'


def reject_requests(modeladmin, request, queryset):
    updated = queryset.filter(status='pending').update(status='rejected')
    modeladmin.message_user(request, f'❌ {updated} درخواست رد شد.', level=messages.WARNING)


reject_requests.short_description = '❌ رد کردن درخواست‌های انتخاب‌شده'


@admin.register(BookSellRequest)
class BookSellRequestAdmin(admin.ModelAdmin):
    list_display   = ['name', 'author_name', 'seller_col', 'category',
                      'price_display', 'stock', 'condition_col', 'status_badge', 'created_at']
    list_filter    = ['status', 'category', 'condition', 'created_at']
    search_fields  = ['name', 'author_name', 'seller__username']
    readonly_fields = ['seller', 'created_at', 'updated_at', 'cover_preview']
    actions        = [approve_and_publish, reject_requests]
    ordering       = ['-created_at']

    fieldsets = (
        ('مشخصات کتاب', {
            'fields': ('name', 'author_name', 'category', 'price', 'stock', 'condition', 'description')
        }),
        ('تصویر جلد', {
            'fields': ('coverpage', 'cover_preview')
        }),
        ('وضعیت درخواست', {
            'fields': ('status', 'admin_note')
        }),
        ('اطلاعات فروشنده', {
            'fields': ('seller', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def seller_col(self, obj):
        return format_html('<b>{}</b>', obj.seller.username)
    seller_col.short_description = 'فروشنده'
    seller_col.admin_order_field = 'seller__username'

    def condition_col(self, obj):
        return obj.get_condition_display()
    condition_col.short_description = 'وضعیت کتاب'

    def price_display(self, obj):
        return f'{obj.price:,} تومان'
    price_display.short_description = 'قیمت'
    price_display.admin_order_field = 'price'

    def status_badge(self, obj):
        colors = {'pending': '#f59e0b', 'approved': '#10b981', 'rejected': '#ef4444'}
        color  = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;'
            'border-radius:10px;font-size:11px">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'وضعیت'

    def cover_preview(self, obj):
        if obj.coverpage:
            return format_html(
                '<img src="{}" style="max-height:180px;border-radius:6px;" />',
                obj.coverpage.url
            )
        return '—'
    cover_preview.short_description = 'پیش‌نمایش جلد'

    def save_model(self, request, obj, form, change):
        if change:
            try:
                old = BookSellRequest.objects.get(pk=obj.pk)
                if old.status != 'approved' and obj.status == 'approved':
                    from store.models import Book, Writer
                    writer = None
                    if obj.author_name:
                        writer_slug = slugify(obj.author_name, allow_unicode=True) or f'writer-{obj.pk}'
                        writer = Writer.objects.filter(slug=writer_slug).first()
                        if not writer:
                            writer = Writer.objects.create(
                                name=obj.author_name,
                                slug=writer_slug,
                                bio=f'کتاب‌فروش: {obj.seller.username}',
                                pic='',
                            )
                    Book.objects.create(
                        writer=writer,
                        category=obj.category,
                        name=obj.name,
                        slug=_create_unique_slug(obj.name),
                        price=obj.price,
                        stock=obj.stock,
                        coverpage=obj.coverpage,
                        bookpage='',
                        description=obj.description,
                        status=0,
                    )
                    self.message_user(
                        request,
                        f'✅ کتاب «{obj.name}» با موفقیت به فروشگاه اضافه شد.',
                        messages.SUCCESS
                    )
            except Exception as e:
                self.message_user(request, f'خطا: {e}', messages.ERROR)
        super().save_model(request, obj, form, change)
