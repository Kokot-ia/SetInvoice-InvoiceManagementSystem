from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:category_id>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:category_id>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Items
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/add/', ItemCreateView.as_view(), name='item_add'),
    path('items/<int:item_id>/edit/', ItemUpdateView.as_view(), name='item_edit'),
    path('items/<int:item_id>/delete/', ItemDeleteView.as_view(), name='item_delete'),
]
