from django.db import models
from django.conf import settings

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='products',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

