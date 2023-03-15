from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


from store.models import Product, Cart, CartItem, Customer, Seller, Address, Order, OrderItem
from .serializer import ProductSerializer, CartSerializer, CustomerSerializer,\
    CartItemSerializer, OrderSerializer, SellerSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from core.serializer import UserCreateSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        # if Product.objects.filter(id=kwargs['pk']).count() > 0:
        #     return Response({'error': 'Product cannot be deleted'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    # queryset = CartItem.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        queryset = CartItem.objects.filter(cart_id=self.kwargs['cart_pk ']).select_related('product')


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'Put':
            serializer = CustomerSerializer(Customer, data=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# class OrderViewSet(ModelViewSet):
#     queryset = OrderSerializer.objects.all()
#     serializer_class = OrderSerializer
