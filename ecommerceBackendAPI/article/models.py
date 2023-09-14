from django.db import models
from our_product.models import Item
# Create your models here.


class ArticleModel(models.Model):
    item_id = models.ForeignKey(
        Item, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
