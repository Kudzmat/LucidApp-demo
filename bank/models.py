from django.utils.timezone import now
from decimal import Decimal
from django.db import models


class BankTransaction(models.Model):
    date = models.DateTimeField(default=now)
    description = models.CharField(max_length=255, blank=False, null=False)
    debit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )
    credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0,
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=False,
        default=0,
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    def calculate_balance(self, current_balance, debit, credit):
        if debit > 0:
            return current_balance - debit
        elif credit > 0:
            return current_balance + credit
        else:
            return current_balance
        
    def __str__(self):
        if self.debit > 0:
            return f"{self.date} - Debit: {self.debit} | {self.transaction} | Balance: {self.balance}"
        elif self.credit > 0:
            return f"{self.date} - Credit: {self.credit} | {self.transaction} | Balance: {self.balance}"
        else:
            return "No transaction"
