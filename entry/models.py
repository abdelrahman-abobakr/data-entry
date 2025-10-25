from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date

class Entry(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('PERSONAL', 'Personal'),
        ('WORK', 'Work'),
        ('EDUCATION', 'Education'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='PERSONAL')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_entries'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Validation rules"""
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        if self.entry_date > date.today():
            raise ValidationError("Date cannot be in the future.")

        # Prevent duplicate submission for same day by same user
        if Entry.objects.filter(user=self.user, entry_date=self.entry_date).exclude(id=self.id).exists():
            raise ValidationError("You already submitted an entry for this date.")

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"
