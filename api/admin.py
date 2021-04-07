from django.contrib import admin

# Register your models here.
from .models import Category, Ingredient, Buyer, Product, Transaction

admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Buyer)
admin.site.register(Product)
admin.site.register(Transaction)