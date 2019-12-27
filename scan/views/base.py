from django.http import Http404
from django.utils.translation import gettext as _
from django.views.generic import DetailView


class IntSlugDetailView(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if not slug.isdigit():
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": self.queryset.model._meta.verbose_name}
            )

        return super().get_object(queryset)
