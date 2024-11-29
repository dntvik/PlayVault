from django.urls import path

from cart.views import CartView, CheckoutView, RemoveFromCartView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="cart_checkout"),
    path("remove_item/<int:item_id>/", RemoveFromCartView.as_view(), name="remove_item"),
]
