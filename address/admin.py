from django.contrib import admin

# Register your models here.
from .models import Country, Province, Wards, Address, District


admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Wards)
admin.site.register(Address)
admin.site.register(District)