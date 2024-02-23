from django.urls import path
from .views import add_category, manage_category
from .views import edit_category, delete_category


urlpatterns = [
    path('add_category/', add_category, name='add_category'),
    path('manage_category/', manage_category, name='manage_category'),
    path('edit_category/<int:pid>/', edit_category, name='edit_category'),

    # Delete Category
    path('delete_category/<int:pid>/', delete_category, name='delete_category'),
]