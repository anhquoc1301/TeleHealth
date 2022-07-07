from django.db import models

# Create your models here.
from django.db import models
from authentication.models import User

class Apartment(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    manage_id = models.CharField(max_length=200)
    apartment_add = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    used = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartment')

    del_flg = models.BooleanField(default=False)
    exclusive_fg = models.BooleanField(default=False)
    created_company_cd = models.IntegerField()
    updated_company_cd = models.IntegerField()
    created_user_id = models.CharField(max_length=100, blank=True, null=True)
    updated_user_id = models.CharField(max_length=100, blank=True, null=True)
    created_user_name = models.CharField(max_length=100, blank=True, null=True)
    updated_user_name = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "apartment"
        ordering = ["created_at"]

    def __str__(self):
        return '{}'.format(self.manage_id)





