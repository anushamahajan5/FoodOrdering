from django.contrib import admin
from .models import (
    Product, 
    ProductMetaInformation, 
    ProductImages, 
    Customer, 
    Order, 
    OrderItem, 
    Restaurant  # Import the Restaurant model
)

# Register models
admin.site.register(Product)
admin.site.register(ProductMetaInformation)
admin.site.register(ProductImages)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)

# Register Restaurant with customization
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  # Customize fields to display
    search_fields = ('name',)  # Enable searching by restaurant name

