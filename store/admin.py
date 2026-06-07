from django.contrib import admin
from .models import Category, Writer, Book, Slider

# ─── عنوان پنل ادمین ─────────────────────────────────────────────────────────
admin.site.site_header = 'پنل مدیریت کتابفروشی شاهد'
admin.site.site_title  = 'کتابفروشی شاهد'
admin.site.index_title = 'خوش آمدید به پنل مدیریت'


class CategoryAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name']

admin.site.register(Category, CategoryAdmin)


class WriterAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name']

admin.site.register(Writer, WriterAdmin)


class BookAdmin(admin.ModelAdmin):
    # ✅ دقیقاً مثل نسخه اصلی — verbose_name مدل‌ها header رو فارسی می‌کنن
    list_display        = ['name', 'price', 'stock', 'status', 'created', 'updated']
    list_filter         = ['status', 'created', 'updated']
    list_editable       = ['price', 'stock', 'status']
    prepopulated_fields = {'slug': ('name',)}
    search_fields       = ['name']

admin.site.register(Book, BookAdmin)


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated']

admin.site.register(Slider, SliderAdmin)
