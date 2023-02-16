from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin


from store.models import Product, Cart, CartItem, Customer, Seller, Address, Order, OrderItem
from .serializer import ProductSerializer, CartSerializer, CustomerSerializer,\
    CartItemSerializer, OrderSerializer, SellerSerializer
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


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


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
