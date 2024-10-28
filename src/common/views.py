from django.views.generic import TemplateView

from games.models import Genre, Platform


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["platforms"] = Platform.objects.all()
        return context
