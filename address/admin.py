from django.contrib import admin

# Register your models here.
from .models import Country, Ethnic, Province, Ward, Address, District


admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Ward)
admin.site.register(Address)
admin.site.register(District)
admin.site.register(Ethnic)