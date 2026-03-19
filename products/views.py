from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description'] # поиск по названию и описанию

    def perform_create(self, serializer):
        # Привязывет владельца к текущему пользователю
        serializer.save(owner=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]


#---------------------------------------
# Просмотр корзины текущего пользователя
# GET /api/products/cart/
#---------------------------------------
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Возвращаем корзину текущего пользователя, создаем если ее нет
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
#---------------------------------------
# Добавление товара в корзину
# POST /api/products/cart/add/
# Тело: JSON: {"product_id": 1, "quantity": 2}
#---------------------------------------
class AddToCartView(generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart, create = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if int(quantity) <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если товар уже есть, увеличиваем количество
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#---------------------------------------
# Удаление товара из корзины
# DELETE /api/products/cart/remove/
# Тело JSON: {"product_id": 1}
#---------------------------------------
class RemoveFromCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        cart = Cart.objects.filter(user=request.user).first()

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        if not cart:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not cart_item:
            return Response({"detail": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item.delete()
        return Response({"detail": "Item removed"}, status=status.HTTP_204_NO_CONTENT)

#---------------------------------------
# Изменение количества товара в корзине
# PATCH /api/products/cart/update/
#---------------------------------------
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        cart = Cart.objects.get(user=request.user)

        cart_item = CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).first()

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        if not quantity:
            return Response({"error": "Quantity is required"}, status=400)

        if int(quantity) <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=400
            )

        if not cart_item:
            return Response(
                {"error": "The product was not found in the cart"},
                status=404
            )
        
        cart_item.quantity = int(quantity)
        cart_item.save()

        return Response({
            "message": "Quantity updated",
            "quantity": cart_item.quantity
        })
    
#---------------------------------------
# Очистка корзины
# DELETE /api/products/cart/clear/
#---------------------------------------
class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = Cart.objects.get(user=request.user)

        cart.items.all().delete()

        return Response({"message": "The Cart has been cleared."})