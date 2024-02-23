from django.urls import path
from . import views
from .views import add_product, manage_product, edit_product, delete_product

urlpatterns = [
    
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('add_product/', add_product, name='add_product'),
    path('manage_product/', manage_product, name='manage_product'),
    path('edit_product/<int:pid>/', edit_product, name='edit_product'),
    path('delete_product/<int:pid>/', delete_product, name='delete_product'),
] 
