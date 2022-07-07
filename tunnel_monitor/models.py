from errno import ESTALE
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

def validate_currency(value):
    if value >= 0:
        return value
    else:
        raise ValidationError("Value must be positive")

class Tunnel(models.Model):
    class Intervals(models.IntegerChoices):
        ONE_MIN = 1, "1 minute"
        FIVE_MIN = 5, "5 minutes"
        FIFTEEN_MIN = 15, "15 minutes"
        ONE_HOUR = 60, "1 hour"
        ONE_DAY = 1440, "1 day"

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=7)
    upper_bound = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_currency])
    lower_bound = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_currency])
    interval = models.IntegerField(choices=Intervals.choices, default=Intervals.FIFTEEN_MIN)
    active = models.BooleanField(default=True)