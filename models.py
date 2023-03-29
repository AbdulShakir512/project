from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
# Create your models here.
class User(AbstractBaseUser):
    username = models.AutoField(primary_key=True)
    email = models.CharField(max_length = 64, unique=True)
    password = models.CharField(max_length = 64)
    role = models.CharField(max_length = 9)
    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    is_active = models.BooleanField(null=False)
    REQUIRED_FIELDS = ['email', 'password', 'role', 'is_staff', 'is_superuser', 'is_active']
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class CurrencyList(models.Model):
    fullName = models.TextField(primary_key=True)
    shortForm = models.CharField(max_length = 5, unique=True)
    amount = models.FloatField()

class form1submitted(models.Model):
    formID = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    control_no = models.TextField()
    applied_by = models.TextField()
    currency_desc = models.TextField()
    purpose = models.TextField()
    date_of_requirement = models.DateField()
    date_of_return = models.DateField()
    state = models.IntegerField()
    approved_by = models.TextField(default=-1)
    finalized_by = models.TextField(default=-1)
    declined_by = models.TextField(default=-1)
    returned = models.BooleanField(default=False)

class form1conversions(models.Model):
    convID = models.AutoField(primary_key=True)
    formID = models.ForeignKey('form1submitted', on_delete=models.CASCADE)
    currency = models.TextField()
    denomination = models.IntegerField()
    no_of_pcs = models.FloatField()
    value_in_local = models.FloatField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['convID', 'formID'], name='unique_convID_formID_combination'
            )
        ]

class form2submitted(models.Model):
    formID = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    orderNo = models.IntegerField()
    control_no = models.TextField()
    currency_desc = models.TextField()
    purpose = models.TextField()
    source = models.TextField()
    share = models.TextField()
    date_of_requirement = models.DateField()
    period = models.TextField()
    state = models.IntegerField()
    approved_by = models.TextField(default=-1)
    finalized_by = models.TextField(default=-1)
    declined_by = models.TextField(default=-1)
    returned = models.BooleanField(default=False)

class form2conversions(models.Model):
    convID = models.AutoField(primary_key=True)
    formID = models.ForeignKey('form2submitted', on_delete=models.CASCADE)
    currency = models.TextField()
    remarks = models.TextField()
    denomination = models.IntegerField()
    no_of_pcs = models.FloatField()
    value_in_local = models.FloatField()
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['convID', 'formID'], name='unique_convID_formID_combination2'
            )
        ]

class logHistory(models.Model):
    logID = models.AutoField(primary_key=True)
    message = models.TextField()