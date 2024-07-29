from django.db import models

class AssetRecord(models.Model):
    description = models.CharField(max_length=255)
    asset_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    serial_number_t24 = models.CharField(max_length=255, blank=True, null=True, default="NOT APPLICABLE")
    nomenclature = models.CharField(max_length=255, unique=True)
    serial_number = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date_purchase = models.DateField()  # Changed to DateField
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    supplier = models.CharField(max_length=255)
    warranty = models.CharField(max_length=255, choices=[('active', 'Active'), ('expired', 'Expired')])
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset_code} - {self.description}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)