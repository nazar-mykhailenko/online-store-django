from django.db import models
from django.contrib.auth.models import User

from core.models import Item


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=8)
    status = models.TextField(blank=True, null=True)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def total(self):
        return self.item.price * self.quantity
