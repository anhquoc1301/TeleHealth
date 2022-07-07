from django.db import models
from authentication.models import User

    # Create your models here.
class Company(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    company_name = models.CharField(max_length=200)
    address_company = models.CharField(max_length=200)
    staff_limit_num = models.IntegerField()
    staff_current_num = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company')

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
        db_table = "company"
        ordering = ["created_at"]


    def __str__(self):
        return '{}'.format(self.company_name)

