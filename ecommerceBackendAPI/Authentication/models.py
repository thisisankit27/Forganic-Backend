from django.db import models
from django.contrib.auth.models import User


class VerifiedEmail(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='verified_emails')
    verified = models.BooleanField(default=False)
