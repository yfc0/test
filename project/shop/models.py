from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)


class Shop(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', null=True,
            on_delete=models.PROTECT, verbose_name='Категория')
    price = models.IntegerField()
    shop = models.ForeignKey('Shop', null=True,
            on_delete=models.PROTECT, verbose_name='Магазин')
    update_counter = models.PositiveIntegerField(default=0)
