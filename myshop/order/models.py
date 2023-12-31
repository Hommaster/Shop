from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal

from products.models import Product
from coupon.models import Coupon


class Order(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=255, blank=True)

    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   default=0)

    def __str__(self):
        return f'Order: {self.id}'

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost_after_discount(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.id)