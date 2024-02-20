from django.contrib import admin

from .models import Product,Offers,SellerDetails,RegisterationRequest


# Register your models here.

admin.site.register(Product)
admin.site.register(Offers)
admin.site.register(SellerDetails)
admin.site.register(RegisterationRequest)

