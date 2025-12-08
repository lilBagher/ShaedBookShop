from django.db import models
from store.models import Book
from django.contrib.auth import get_user_model
class Order(models.Model):
	customer = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
	name = models.CharField(max_length=30)
	email = models.EmailField()
	phone = models.CharField(max_length=16)
	
	# ✅ تغییر: این فیلدها اکنون اختیاری هستند
	address = models.CharField(max_length=150, blank=True, null=True)
	division = models.CharField(max_length=20, blank=True, null=True)
	district = models.CharField(max_length=30, blank=True, null=True)
	zip_code = models.CharField(max_length=30, blank=True, null=True)
	
	# ✅ تغییر: این فیلدها هم اختیاری شدند
	payment_method = models.CharField(max_length = 20, blank=True, null=True)
	account_no = models.CharField(max_length = 20, blank=True, null=True)

	# ✅ تغییر مهم: این فیلد را به CharField تغییر دادیم تا کد رهگیری متنی زرین‌پال در آن ذخیره شود
	transaction_id = models.CharField(max_length=100, blank=True, null=True) 
	
	payable = models.IntegerField()
	totalbook = models.IntegerField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)

	class Meta:
		ordering = ('-created', )

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
