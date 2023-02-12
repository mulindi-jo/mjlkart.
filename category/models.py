from django.db import models
from django.urls import reverse

from cache.models import DefaultField

class Category(DefaultField):
    name = models.CharField(max_length=50, unique=True, blank=False)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=False)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name
