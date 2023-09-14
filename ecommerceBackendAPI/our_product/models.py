from django.db import models
from django.core.validators import MaxValueValidator


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    discount_amount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    availability = models.BooleanField(default=True)
    rating = models.DecimalField(
        validators=[MaxValueValidator(5)], max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Comments(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
