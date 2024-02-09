from django.contrib import admin

from .models import Product,Offers,SellerDetails


# Register your models here.

admin.site.register(Product)
admin.site.register(Offers)
admin.site.register(SellerDetails)

