from django.db import models

from cache.models import DefaultField
from store.models import Product


class Cart(DefaultField):
    cart_id = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.id

class CartItem(DefaultField):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity =models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
