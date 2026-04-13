from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import PainPointForm
from .models import Category, PainPoint
from .utils.markdown import render_markdown


class IndexView(TemplateView):
    template_name = 'collaboration/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class PainPointListView(ListView):
    model = PainPoint
    template_name = 'collaboration/painpoint_list.html'
    context_object_name = 'pain_points'
    paginate_by = 20

    def get_queryset(self):
        qs = PainPoint.objects.select_related('author', 'category').order_by('-created_at')
        slug = self.request.GET.get('category')
        if slug:
            qs = qs.filter(category__slug=slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['current_category'] = self.request.GET.get('category', '')
        return ctx


class PainPointDetailView(DetailView):
    model = PainPoint
    template_name = 'collaboration/painpoint_detail.html'
    context_object_name = 'pain_point'

    def get_queryset(self):
        return PainPoint.objects.select_related('author', 'category')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pp = self.object
        ctx['context_html'] = render_markdown(pp.context)
        ctx['current_solution_html'] = render_markdown(pp.current_solution)
        ctx['potential_value_html'] = render_markdown(pp.potential_value)
        return ctx


class PainPointCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PainPoint
    form_class = PainPointForm
    template_name = 'collaboration/painpoint_form.html'

    def test_func(self):
        profile = getattr(self.request.user, 'profile', None)
        return profile is not None and profile.role == profile.Role.EXPERT

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, '痛點已發布。')
        return response

    def get_success_url(self):
        return reverse('painpoint_detail', kwargs={'pk': self.object.pk})
