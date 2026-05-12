from django.views.generic import TemplateView

from bendy_app.models import BendyUser


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_users"] = BendyUser.objects.filter(is_active=True).order_by(
            "-joined_at")[:5]
        context["top_contributors"] = BendyUser.objects.filter(
            is_active=True).order_by("-ink_points")[:5]
        return context