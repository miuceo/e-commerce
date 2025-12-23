from django.urls import path
from .views import (HomePageView,
                    AboutPageView,
                    ShopPageView,
                    CartPageView,
                    ShopDetailsPageView,
                    CheckoutPageView,
                    ContactPageView,)

urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("about/", AboutPageView.as_view(), name='about'),
    path("shop/", ShopPageView.as_view(), name='shop'),
    path("shopping-cart/", CartPageView.as_view(), name='cart'),
    path("shop-details/", ShopDetailsPageView.as_view(), name='shop-detail'),
    path("checkout/", CheckoutPageView.as_view(), name='checkout'),
    path("contact/", ContactPageView.as_view(), name='contact'),
]
