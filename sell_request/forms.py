from django import forms
from .models import BookSellRequest


class BookSellRequestForm(forms.ModelForm):
    class Meta:
        model = BookSellRequest
        fields = ['name', 'author_name', 'category', 'price', 'stock',
                  'description', 'coverpage', 'condition']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کتاب را وارد کنید'
            }),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام نویسنده'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 85000'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'توضیحات کتاب (اختیاری)'
            }),
            'coverpage': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'نام کتاب',
            'author_name': 'نام نویسنده',
            'category': 'دسته‌بندی',
            'price': 'قیمت (تومان)',
            'stock': 'تعداد موجودی',
            'description': 'توضیحات',
            'coverpage': 'تصویر جلد',
            'condition': 'وضعیت کتاب',
        }
