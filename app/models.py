from django.db import models

# Create your models here.
class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20)
    amount = models.IntegerField()
    merchant_id = models.CharField(max_length=100)
    check_id = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)