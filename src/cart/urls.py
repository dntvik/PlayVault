from django.urls import path

from cart.views import CartView, CheckoutView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="cart_checkout"),
]
