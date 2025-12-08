# order/views.py
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .pdfcreator import renderPdf
from django.urls import reverse
import arabic_reshaper
from bidi.algorithm import get_display
import time
# from azbankgateways import bankfactories, models as bank_models, default_settings as settings
# import azbankgateways.exceptions as bank_exceptions

def order_create(request):
	cart = Cart(request)
	if request.user.is_authenticated:
		customer = get_object_or_404(User, id=request.user.id)
		form = OrderCreateForm(request.POST or None, initial={"name": customer.first_name, "email": customer.email})

		if request.method == 'POST':
			if form.is_valid():
				order = form.save(commit=False)
				order.customer = User.objects.get(id=request.user.id)
				order.payable = cart.get_total_price()
				order.totalbook = len(cart)
				# سفارش با وضعیت "پرداخت نشده" ذخیره می‌شود
				order.save()

				for item in cart:
					OrderItem.objects.create(
						order=order,
						book=item['book'],
						price=item['price'],
						quantity=item['quantity']
						)

				# آیدی سفارش را در سشن ذخیره می‌کنیم
				request.session['order_id'] = order.id

				# ✅ تغییر: کاربر را به صفحه درگاه پرداخت جعلی هدایت می‌کنیم
				return redirect('order:fake_payment_page')

			else:
				messages.error(request, "لطفا اطلاعات خود را به درستی وارد کنید.")

		if len(cart) > 0:
			return render(request, 'order/order.html', {"form": form})
		else:
			return redirect('store:books')
	else:
		return redirect('store:signin')

#
# ✅ تابع جدید: نمایش صفحه درگاه پرداخت جعلی
#
def fake_payment_page(request):
	cart = Cart(request)
	order_id = request.session.get('order_id')
	if not order_id:
		return redirect('store:books') # اگر سفارش وجود نداشت، به فروشگاه برگرد

	order = get_object_or_404(Order, id=order_id)
	# ما فقط مبلغ را به صفحه پرداخت جعلی می‌فرستیم
	context = {
		'amount': cart.get_total_price(),
	}
	return render(request, 'order/fake_gateway.html', context)

#
# ✅ تابع جدید: مدیریت پرداخت موفق
#
def payment_success(request):
	order_id = request.session.get('order_id')
	if not order_id:
		return redirect('store:books')

	order = get_object_or_404(Order, id=order_id)
	cart = Cart(request)

	# ✅ سفارش در دیتابیس ثبت می‌شود (وضعیت پرداخت آپدیت می‌شود)
	# ✅ تورفتگی‌های اشتباه در این 3 خط اصلاح شد
	order.paid = True
	order.transaction_id = f"FAKE-{int(time.time())}-{order.id}"
	order.save()

	# سبد خرید خالی می‌شود
	cart.clear()
	# سشن پاک می‌شود
	del request.session['order_id']

	# کاربر به صفحه موفقیت‌آمیز هدایت می‌شود
	# این صفحه از قبل کد پیگیری (order.id) را نشان می‌داد
	return render(request, 'order/successfull.html', {'order': order})

#
# ✅ تابع جدید: مدیریت پرداخت ناموفق
#
def payment_fail(request):
	order_id = request.session.get('order_id')
	if not order_id:
		return redirect('store:books')

	order = get_object_or_404(Order, id=order_id)

	# ✅ عدم ثبت سفارش: سفارش و آیتم‌های مربوط به آن از دیتابیس حذف می‌شوند
	order.delete()

	# سشن پاک می‌شود
	del request.session['order_id']

	messages.error(request, "پرداخت ناموفق بود. سفارش شما ثبت نشد و لغو گردید.")
	# کاربر به سبد خرید بازگردانده می‌شود
	return redirect('cart:cart_details')

#
# بقیه توابع شما (order_list, order_details, pdf) بدون تغییر باقی می‌مانند
#
def order_list(request):
# ... (کد شما بدون تغییر) ...
	my_order = Order.objects.filter(customer_id = request.user.id).order_by('-created')
	paginator = Paginator(my_order, 5)
	page = request.GET.get('page')
	myorder = paginator.get_page(page)

	return render(request, 'order/list.html', {"myorder": myorder})

def order_details(request, id):
# ... (کد شما بدون تغییر) ...
	order_summary = get_object_or_404(Order, id=id)

	if order_summary.customer_id != request.user.id:
		return redirect('store:index')

	orderedItem = OrderItem.objects.filter(order_id=id)
	context = {
		"o_summary": order_summary,
		"o_item": orderedItem
	}
	return render(request, 'order/details.html', context)

class pdf(View):
    def get(self, request, id):
        try:
            query = get_object_or_404(Order, id=id)
        except:
            raise Http404('Content not found')

        # --- ✅ بخش جدید: پردازش متن فارسی ---

        # تابع کمکی برای پردازش
        def shape_farsi(text):
            if text:
                return get_display(arabic_reshaper.reshape(str(text)))
            return text

        # آماده‌سازی آیتم‌های کتاب با نام‌های پردازش شده
        shaped_items = []
        for item in query.orderitem_set.all():
            shaped_items.append({
                'name': shape_farsi(item.book.name),
                'quantity': shape_farsi(item.quantity),
                'price': shape_farsi(item.price),
                'total': shape_farsi(item.get_cost())
            })

        # آماده‌سازی تمام متن‌های ثابت فارسی
        context = {
            "order": query,
            "shaped_items": shaped_items,
            "farsi": {
                "header_title": shape_farsi("فروشگاه کتاب"),
                "header_subtitle": shape_farsi("کد پیگیری سفارش (جهت تحویل):"),
                "order_id": shape_farsi(f"#{query.id}"),
                "info_title": shape_farsi("اطلاعات گیرنده"),
                "name_label": shape_farsi("نام:"),
                "name_value": shape_farsi(query.name),
                "email_label": shape_farsi("ایمیل:"),
                "phone_label": shape_farsi("شماره تماس:"),
                "details_title": shape_farsi("جزئیات سفارش"),
                "status_label": shape_farsi("وضعیت پرداخت:"),
                "status_value": shape_farsi("پرداخت شده" if query.paid else "ناموفق"),
                "date_label": shape_farsi("تاریخ سفارش:"),
                "tx_label": shape_farsi("کد رهگیری بانک:"),
                "items_title": shape_farsi("کتاب‌های سفارش داده شده"),
                "th_name": shape_farsi("نام کتاب"),
                "th_qty": shape_farsi("تعداد"),
                "th_price": shape_farsi("قیمت واحد"),
                "th_total": shape_farsi("جمع کل"),
                "total_1": shape_farsi("جمع کل کتاب‌ها:"),
                "total_2": shape_farsi("هزینه ارسال:"),
                "total_3": shape_farsi("مبلغ نهایی پرداخت شده:"),
                "toman": shape_farsi("تومان"),
                "zero": shape_farsi("۰"),
            }
        }
        article_pdf = renderPdf('order/pdf.html', context)
        return HttpResponse(article_pdf, content_type='application/pdf')