from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    ]
    age = models.PositiveIntegerField(null=True, blank=True)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return f"{self.username} ({self.role})"
