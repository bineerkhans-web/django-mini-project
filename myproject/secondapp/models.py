from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Plot(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='plots',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    seller_name = models.CharField(max_length=100)
    seller_phone = models.CharField(max_length=15)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    cent = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    map_address = models.CharField(max_length=255, blank=True, null=True, help_text="Full address for map (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def primary_image_url(self):
        first_image = self.images.first()
        if first_image and first_image.image:
            return first_image.image.url
        return None
    
    @property
    def total_price(self):
        """Calculate total price (price per cent * cent)"""
        return float(self.price) * float(self.cent)

class PlotImage(models.Model):
    plot = models.ForeignKey(Plot, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plot_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.plot.title}"
