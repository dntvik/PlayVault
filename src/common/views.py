from django.views.generic import TemplateView

from accounts.models import Customer
from games.models import Genre, Platform


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["platforms"] = Platform.objects.all()
        if self.request.user.is_authenticated:
            context["user_profile"] = self.request.user.profile
        else:
            context["user_profile"] = None

        return context
