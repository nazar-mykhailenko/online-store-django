from django.db import models
from django.contrib.auth.models import User
from core.models import Item


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def get_total(self):
        return self.quantity * self.product.price

    class Meta:
        unique_together = (('user', 'product'),)
