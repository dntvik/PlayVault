from django.views.generic import TemplateView

from accounts.models import Customer
from cart.models import Cart
from games.models import Genre, Platform


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["platforms"] = Platform.objects.all()
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart and cart.items.count() > 0:
                context["cart"] = cart
            else:
                context["cart"] = None
        if self.request.user.is_authenticated:
            context["user_profile"] = self.request.user
        else:
            context["user_profile"] = None

        return context
