from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner, IsAdmin
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
    
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Получаем корзину
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty"}, status=400)
        
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"error": "Cart is empty"}, status=400)
        
        # Атомарность
        with transaction.atomic():
            order = Order.objects.create(user=user)

            total_price = 0

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                total_price += item.product.price * item.quantity
            
            order.total_price = total_price
            order.save()

            # Очищаем корзину
            cart.items.all().delete()
        
        return Response({"message": "Order created successfully"})

# Список закаказов пользователя
class OrderListView(generics.ListAPIView): 
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
# Просмотр одного заказа
class OrderDetailView(generics.RetrieveAPIView):
    serialiser_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.all()
    
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()

        return Order.objects.filter(user=self.request.user)

class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        new_status = request.data.get("status")

        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=404
            )
        
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]

        if new_status not in valid_statuses:
            return Response(
                {"error": "Invalid status"},
                status=400
            )
        
        order.status = new_status
        order.save()

        return Response({
            "message": "Status updated",
            "status": order.status
        })
    
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        return Order.objects.filter(user=user)