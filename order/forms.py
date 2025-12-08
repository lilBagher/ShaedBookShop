from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):

    # ✅ 1. فیلدها را در اینجا (خارج از Meta) بازنویسی می‌کنیم
    # تا بتوانیم پیام‌های خطا و لیبل فارسی را اضافه کنیم

    name = forms.CharField(
        label='نام و نام خانوادگی',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'وارد کردن نام و نام خانوادگی الزامی است.',
        }
    )
    email = forms.EmailField(
        label='آدرس ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'وارد کردن آدرس ایمیل الزامی است.',
            'invalid': 'لطفاً یک آدرس ایمیل معتبر وارد کنید.',
        }
    )
    phone = forms.CharField(
        label='شماره تماس (برای پیگیری)',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'وارد کردن شماره تماس الزامی است.',
        }
    )

    class Meta:
        model = Order
        # ✅ فیلدها همچنان اینجا لیست می‌شوند
        fields = ['name', 'email', 'phone']