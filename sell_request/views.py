from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BookSellRequest
from .forms import BookSellRequestForm


@login_required(login_url='/login')
def submit_sell_request(request):
    """صفحه ثبت درخواست فروش کتاب توسط کاربر"""
    if request.method == 'POST':
        form = BookSellRequestForm(request.POST, request.FILES)
        if form.is_valid():
            sell_request = form.save(commit=False)
            sell_request.seller = request.user
            sell_request.save()
            messages.success(
                request,
                'درخواست فروش شما با موفقیت ثبت شد. پس از تأیید توسط مدیریت، کتاب شما به فروشگاه اضافه خواهد شد.'
            )
            return redirect('sell_request:my_requests')
    else:
        form = BookSellRequestForm()

    return render(request, 'sell_request/submit.html', {'form': form})


@login_required(login_url='/login')
def my_sell_requests(request):
    """لیست درخواست‌های فروش کاربر جاری"""
    requests_qs = BookSellRequest.objects.filter(seller=request.user)
    paginator = Paginator(requests_qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'sell_request/my_requests.html', {'page_obj': page_obj})


@login_required(login_url='/login')
def sell_request_detail(request, pk):
    """جزئیات یک درخواست فروش"""
    sell_req = get_object_or_404(BookSellRequest, pk=pk, seller=request.user)
    return render(request, 'sell_request/detail.html', {'sell_request': sell_req})


@login_required(login_url='/login')
def delete_sell_request(request, pk):
    """حذف درخواست فروش (فقط درخواست‌های pending)"""
    sell_req = get_object_or_404(BookSellRequest, pk=pk, seller=request.user)
    if sell_req.status == 'pending':
        sell_req.delete()
        messages.success(request, 'درخواست فروش با موفقیت حذف شد.')
    else:
        messages.error(request, 'امکان حذف این درخواست وجود ندارد.')
    return redirect('sell_request:my_requests')
