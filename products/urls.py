from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]