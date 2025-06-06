from django.db import models

# Create your models here.


class AssetType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Assets(models.Model):
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    brand_model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    supplier_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_cell = models.CharField(max_length=20)
    po_date = models.DateField()
    purchase_date = models.DateField()
    warranty_start_date = models.DateField()
    warranty_expiry_date = models.DateField()
   
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.asset_type.name} - {self.serial_number}"




class DamagedAssets(models.Model):
    asset_type = models.CharField(max_length=100)
    brand_model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_cell = models.CharField(max_length=20)
    purchase_date = models.DateField()
    warranty_start_date = models.DateField(null=True, blank=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    po_date = models.DateField(null=True, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"Damaged: {self.asset_type} - {self.brand_model} ({self.serial_number})"



class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Allocation(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=100)

    # Fields copied from Assets
    asset_type = models.CharField(max_length=100)
    brand_model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_cell = models.CharField(max_length=20)
    purchase_date = models.DateField()
    warranty_start_date = models.DateField()
    warranty_expiry_date = models.DateField()
    po_date = models.DateField()
    comments = models.TextField(blank=True, null=True)

    maintenance_date = models.DateField()

    def __str__(self):
        return f"{self.asset_type} - {self.serial_number} ({self.employee_name})"
