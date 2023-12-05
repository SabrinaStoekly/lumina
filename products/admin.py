from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'sku')
    list_filter = ('category',)  # Adiciona filtro por categoria
    search_fields = ('name', 'description')  # Adiciona campo de pesquisa por nome e descrição

