from django.utils.timezone import now
from decimal import Decimal
from django.db import models

class StorePurchase(models.Model):
    date = models.DateTimeField(default=now)
    item = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="The name of the item being purchased"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The cost of the item in USD"
    )
    quantity = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="The number of items being purchased"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The total cost of the purchase in USD",
        default=Decimal('0.00')
    )
    customer_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="The name of the customer making the purchase"
    )
    customer_email = models.EmailField(
        blank=False,
        null=False,
        help_text="The email address of the customer"
    )
    customer_address = models.CharField(
        max_length=255,
        default="N/A",
        blank=True,
        null=False,
        help_text="The address of the customer"
    )
    sold_by = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="The name of the person who sold the item"
    )

    def save(self, *args, **kwargs):
        self.total = self.amount * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.item} - {self.quantity} @ ${self.amount} each, Total: ${self.total}, Customer: {self.customer_name}"
    class Meta:
        verbose_name = "Store Purchase"
        verbose_name_plural = "Store Purchases"

class OnlinePurchase(StorePurchase):
    sold_by = None  # No need to specify sold_by for online purchases
    assigned_to = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="The name of the person assigned to handle the online purchase"
    )
    delivery_method = models.CharField(
        max_length=50,
        choices=[
            ('standard', 'Standard Shipping'),
            ('express', 'Express Shipping'),
            ('pickup', 'In-Store Pickup')
        ],
        default='standard',
        help_text="The method of delivery for the purchase"
    )
    channel = models.CharField(
        max_length=50,
        choices=[
            ('website', 'Website'),
            ('whatsapp', 'WhatsApp'),
            ('instagram', 'Instagram')
        ],
        default='website',
        help_text="The channel through which the purchase was made"
    )
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The tracking number for the shipment, if applicable"
    )
    delivered = models.BooleanField(
        default=False,
        help_text="Indicates if the online purchase has been delivered"
    )
    
    def __str__(self):
        return f"{super().__str__()}, Delivery Method: {self.delivery_method}, Tracking Number: {self.tracking_number or 'N/A'}"
    
    class Meta:
        verbose_name = "Online Purchase"
        verbose_name_plural = "Online Purchases"
