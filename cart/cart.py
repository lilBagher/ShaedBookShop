# cart/cart.py
from decimal import Decimal
from django.conf import settings
from store.models import Book


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity=None):
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}

        if quantity:
            # اگر تعداد مشخص شده بود (از صفحه cart.html)
            self.cart[book_id]['quantity'] = quantity
        else:
            # اگر از دکمه "افزودن" بود (از صفحه index.html)
            if self.cart[book_id]['quantity'] < 10:
                self.cart[book_id]['quantity'] += 1

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        """
        این متد بازنویسی شده تا سشن را مستقیماً تغییر ندهد.
        """
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)

        book_lookup = {str(book.id): book for book in books}

        # روی یک کپی از آیتم‌های سشن لوپ می‌زنیم
        for book_id, session_item in self.cart.items():
            if book_id in book_lookup:
                # یک دیکشنری "کپی" جدید برای هر آیتم می‌سازیم
                item = session_item.copy() # <-- این خط کپی، کلید حل مشکل است

                # آبجکت کتاب و قیمت‌های محاسبه شده را به این "کپی" اضافه می‌کنیم
                item['book'] = book_lookup[book_id]
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']

                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # این تابع فقط محاسبه می‌کند و در سشن ذخیره نمی‌کند، پس امن است
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True