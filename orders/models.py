from django.utils.timezone import now
from decimal import Decimal
from django.db import models
from sales.models import Inventory  # Import the Inventory model

# Create your models here.
class StoreOrder(models.Model):
    date = models.DateTimeField(default=now)

    # Change item field to a ForeignKey
    item = models.ForeignKey(
        Inventory,  # Reference the Inventory model
        on_delete=models.CASCADE,  # Delete the order if the inventory item is deleted
        help_text="The inventory item being ordered"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        help_text="The cost of the item in USD"
    )
    quantity = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="The number of items being ordered"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        help_text="The total cost of the order in USD",
        default=Decimal('0.00')
    )

    delivered = models.BooleanField(
        default=False,
        help_text="Indicates if the order has been delivered to us" 
    )
    
    def save(self, *args, **kwargs):
        self.total = self.amount * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.item} - {self.quantity} @ ${self.amount} each, Total Cost: ${self.total}"
    class Meta:
        verbose_name = "Store Order"
        verbose_name_plural = "Store Orders"