from django.contrib import admin
from .models import Plot, PlotImage

class PlotImageInline(admin.TabularInline):
    model = PlotImage
    extra = 1

@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller_name', 'location', 'cent', 'price', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['title', 'seller_name', 'location', 'description']
    inlines = [PlotImageInline]

@admin.register(PlotImage)
class PlotImageAdmin(admin.ModelAdmin):
    list_display = ['plot', 'image', 'created_at']
    list_filter = ['created_at']
