from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CartView, AddToCartView, RemoveFromCartView, UpdateCartItemView, ClearCartView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='cart-remove'),
    path('cart/update/', UpdateCartItemView.as_view()),
    path('cart/clear/', ClearCartView.as_view()),
]
