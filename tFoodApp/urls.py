from rest_framework.routers import DefaultRouter
from .views import (
    CategoryView,
    CreateCategoryView,
    ProductView,
    CreateProductView,
    AddtoCartView,
    DeleteFromCartView,
    OrderCartView,
)

router = DefaultRouter()

router.register('categories', CategoryView, basename='categories')
router.register('create-categories', CreateCategoryView, basename='create-categories')
router.register('products', ProductView, basename='products')
router.register('create-product', CreateProductView, basename='create-product')
router.register('add-product', AddtoCartView, basename='add-product')
router.register('delete-product', DeleteFromCartView, basename='delete-product')
router.register('order', OrderCartView, basename='order')


urlpatterns = router.urls
