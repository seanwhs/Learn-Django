# store -- main app -- models.py
from django.db import models

class Promotion(models.Model):
    # Discount rule applied to products
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    # Groups products under a named collection/category
    title = models.CharField(max_length=255)
    # Featured product without creating reverse relation on Product
    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )


class Product(models.Model):
    # Main product catalog entry
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # Prevent deleting a collection if products still reference it
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # A product may have multiple promotions
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    # Membership levels for customers
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]

    # Customer personal information
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # Customer membership tier
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=MEMBERSHIP_BRONZE
    )


class Order(models.Model):
    # Order payment states
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    # When the order was placed
    palced_at = models.DateTimeField(auto_now_add=True)
    # Payment result/status
    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING
    )
    # Keep order history even if customer is removed
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # A single line item within an order
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)


class Address(models.Model):
    # Customer shipping or billing address
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # Delete all addresses when customer is deleted
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    # Shopping cart associated with session or user
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # Products inside a cart
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
