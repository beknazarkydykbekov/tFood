from rest_framework.viewsets import ModelViewSet, mixins
from .models import *
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartProductSerializer, DeleteCartProductSerializer, OrderSerializer
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, permissions
from tFoodApp.utils import recalc_cart


class CategoryView(ModelViewSet):
    http_method_names = ['get', 'head']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.AllowAny
    ]


class CreateCategoryView(ModelViewSet):
    http_method_names = ['post', 'create']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class ProductView(ModelViewSet):
    http_method_names = ['get', 'head']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [
        permissions.AllowAny
    ]


class CreateProductView(ModelViewSet):
    http_method_names = ['post', 'create']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class AddtoCartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.all(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.product.add(cart_product)
        recalc_cart(self.cart)


class DeleteFromCartView(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    http_method_names = ['delete']
    serializer_class = DeleteCartProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.all(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)


class OrderCartView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    http_method_names = ['post', 'get']
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = Order(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if order.is_valid():
            new_order = order.save(commit=False)
            new_order.customer = customer
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)