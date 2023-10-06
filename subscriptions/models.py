from django.db import models


# Create your models here.
class SubscriptionPlan(models.Model):
    plan_name = models.CharField(max_length=150)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_summary = models.CharField(max_length=200, default="No Summary Available")

    def __str__(self):
        return self.plan_name

