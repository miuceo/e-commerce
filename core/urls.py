from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("about/", views.AboutPageView.as_view(), name='about'),
    path("shop/", views.ShopPageView.as_view(), name='shop'),
    path("shopping-cart/", views.CartPageView.as_view(), name='cart'),
    path("shop-details/", views.ShopDetailsPageView.as_view(), name='shop-detail'),
    path("checkout/", views.CheckoutPageView.as_view(), name='checkout'),
    path("contact/", views.ContactPageView.as_view(), name='contact'),
]
