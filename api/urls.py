from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (CustomTokenObtainPairView, 
                    HomePageView, 
                    UserRegister,
                    AdminUsersView,
                    AdminCategoryView,
                    AdminBrandView,
                    AdminSizeView,
                    AdminBlogView,
                    AdminTagView,
                    ProductsView,
                    SellerProductView,
                    UserCartViews,
                    NonOrderCartView,
                    OrdersView)

router = DefaultRouter()
router.register('admin/users', AdminUsersView, basename="admin-users")
router.register('admin/categories', AdminCategoryView, basename="admin-categories")
router.register('admin/brands', AdminBrandView, basename="admin-brands")
router.register('admin/size', AdminSizeView, basename="admin-size")
router.register('admin/tags', AdminTagView, basename="admin-tag")
router.register('admin/blog', AdminBlogView, basename="admin-blog")
router.register('seller-admin/products', SellerProductView, basename="seller-products")
router.register('register', UserRegister, basename='register-user')
router.register('user/products', ProductsView, basename="products")
router.register('user/cart', UserCartViews, basename="cart-items")
router.register('user/non-order-cart', NonOrderCartView, basename="cart-items-non-order")
router.register('user/orders', OrdersView, basename="user-orders")

app_name = "api"

urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name="token"),
    path('auth/refresh/', TokenRefreshView.as_view(), name="refresh"),
    
    path('', HomePageView.as_view(), name="home"),
    *router.urls
]

  