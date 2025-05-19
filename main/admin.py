from django.contrib import admin
from .models import Products, ProductImage,Book_Service,Contact_form


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Allows adding up to 3 extra images

class ProductsAdmin(admin.ModelAdmin):
    list_display=["name","price","category","latest_items","bestseller"]    

    inlines = [ProductImageInline]

admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductImage)
admin.site.register(Book_Service)
admin.site.register(Contact_form)
# admin.site.register(Size)