from django.db import models
import uuid

# BaseModel with reusable fields
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Corrected auto_add
    updated_at = models.DateTimeField(auto_now=True)      # Corrected auto_add

    class Meta:
        abstract = True

class Restaurant(BaseModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField(null=True, blank=True)

class Product(BaseModel):
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name="products",
        default=1  # Replace 1 with the ID of an existing restaurant
    )
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(unique=True)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_actual_price = models.DecimalField(max_digits=10, decimal_places=2)

# Customer Model
class Customer(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

# Order Model
class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through='OrderItem')  # Correct Many-to-Many
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50, choices=(('Pending', 'Pending'), ('Completed', 'Completed'))
    )
    delivery_date = models.DateField(null=True, blank=True)

# Intermediary Model for Many-to-Many Relationship
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# Product Meta Information
class ProductMetaInformation(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="meta_info")
    product_quantity = models.CharField(max_length=50, null=True, blank=True)  # Added max_length
    product_weight = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=(("kg", "kg"), ("ml", "ml"), ("l", "l"), (None, None))
    )

# Product Images
class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    product_images = models.ImageField(upload_to='products')
