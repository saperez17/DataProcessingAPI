from django.db import models
# from django_mysql.models import JSONField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Buyer(models.Model):
    buyer = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.buyer}, {self.name}, {self.age}"

class Product(models.Model):
    product  = models.CharField(max_length=100)
    name = models.CharField(max_length=300, blank=True)
    price = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.product}, {self.name}, {self.price}"

class Transaction(models.Model):
    transaction = models.CharField(max_length=50)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name="buyer_transactions", blank=False)
    # buyer = models.CharField(max_length=500)    
    ip = models.CharField(max_length=100)
    device = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_transactions", blank=False)
    # product = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.transaction}, {self.buyer}, {self.ip}, {self.device}, {self.product}"