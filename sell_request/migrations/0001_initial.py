from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('store', '0002_alter_book_writer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSellRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام کتاب')),
                ('author_name', models.CharField(max_length=200, verbose_name='نام نویسنده')),
                ('price', models.IntegerField(verbose_name='قیمت (تومان)')),
                ('stock', models.IntegerField(default=1, verbose_name='تعداد موجودی')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('coverpage', models.FileField(upload_to='sell_requests/covers/', verbose_name='تصویر جلد کتاب')),
                ('condition', models.CharField(
                    choices=[('new', 'نو'), ('like_new', 'در حد نو'), ('good', 'خوب'), ('acceptable', 'قابل قبول')],
                    default='good', max_length=20, verbose_name='وضعیت کتاب'
                )),
                ('status', models.CharField(
                    choices=[('pending', 'در انتظار بررسی'), ('approved', 'تأیید شده'), ('rejected', 'رد شده')],
                    default='pending', max_length=10, verbose_name='وضعیت درخواست'
                )),
                ('admin_note', models.TextField(blank=True, verbose_name='توضیحات ادمین')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')),
                ('seller', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sell_requests',
                    to='auth.user',
                    verbose_name='فروشنده'
                )),
                ('category', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='store.category',
                    verbose_name='دسته‌بندی'
                )),
            ],
            options={
                'verbose_name': 'درخواست فروش کتاب',
                'verbose_name_plural': 'درخواست‌های فروش کتاب',
                'ordering': ['-created_at'],
            },
        ),
    ]
