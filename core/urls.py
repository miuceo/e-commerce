from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("about/", views.AboutPageView.as_view(), name='about'),
    path("shop/", views.ShopPageView.as_view(), name='shop'),
    path("shopping-cart/", views.cartpageview, name='cart'),
    path("shopping-cart/update", views.cartupdateview, name='cart-update'),
    path("shopping-cart/<int:id>/", views.cartdeleteview, name='cart-delete'),
    path("checkout/", views.checkoutview, name='checkout'),
    path("checkout/create/", views.create_order, name='create_order'),
    path('orders/', views.orderview, name="orders"),
    path('orders/<int:id>/', views.deleteorder, name="order-delete"),
    path("shop-details/<str:slug>", views.ShopDetailsPageView.as_view(), name='shop-detail'),
    path("contact/", views.ContactPageView.as_view(), name='contact'),
]
