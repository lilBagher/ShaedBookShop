from django.db import models


class Category(models.Model):
    name       = models.CharField(max_length=100, verbose_name='نام')
    slug       = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='شناسه URL')
    icon       = models.FileField(upload_to='category/', verbose_name='آیکون')
    create_at  = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='آخرین به‌روزرسانی')

    class Meta:
        verbose_name        = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name


class Writer(models.Model):
    name       = models.CharField(max_length=100, verbose_name='نام')
    slug       = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='شناسه URL')
    bio        = models.TextField(verbose_name='بیوگرافی')
    pic        = models.FileField(upload_to='writer/', verbose_name='تصویر')
    create_at  = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='آخرین به‌روزرسانی')

    class Meta:
        verbose_name        = 'نویسنده'
        verbose_name_plural = 'نویسندگان'

    def __str__(self):
        return self.name


class Book(models.Model):
    writer      = models.ForeignKey(Writer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='نویسنده')
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته‌بندی')
    name        = models.CharField(max_length=100, verbose_name='نام کتاب')
    slug        = models.SlugField(max_length=100, db_index=True, verbose_name='شناسه URL')
    price       = models.IntegerField(verbose_name='قیمت (تومان)')
    stock       = models.IntegerField(verbose_name='موجودی')
    coverpage   = models.FileField(upload_to='coverpage/', verbose_name='تصویر جلد')
    bookpage    = models.FileField(upload_to='bookpage/', verbose_name='فایل کتاب')
    created     = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated     = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')
    status      = models.IntegerField(default=0, verbose_name='وضعیت')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name        = 'کتاب'
        verbose_name_plural = 'کتاب‌ها'

    def __str__(self):
        return self.name


class Slider(models.Model):
    title    = models.CharField(max_length=150, verbose_name='عنوان')
    created  = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated  = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')
    slideimg = models.FileField(upload_to='slide/', verbose_name='تصویر اسلاید')

    class Meta:
        verbose_name        = 'اسلاید'
        verbose_name_plural = 'اسلایدها'

    def __str__(self):
        return self.title
