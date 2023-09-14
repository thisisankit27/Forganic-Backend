from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:pk>/',
         views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('list-cart/', views.ListCartView.as_view(), name='list_cart'),
    path('update-cart-item-quantity/<int:pk>/',
         views.UpdateCartItemQuantityView.as_view(), name='update_cart_item_quantity'),
]
