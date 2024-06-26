from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from .models import Nota, Viagem
from .forms import ViagemForm, NotaForm
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date

class HomeView(TemplateView):
    template_name = 'notas/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viagens'] = Viagem.objects.all()
        viagem_id = self.request.GET.get('viagem_id')
        if viagem_id:
            context['notas'] = Nota.objects.filter(viagem_id=viagem_id)
            context['selected_viagem'] = Viagem.objects.get(id=viagem_id)
        else:
            context['notas'] = None
            context['selected_viagem'] = None
        return context

class ViagemListView(ListView):
    model = Viagem
    template_name = 'notas/pages/viagem_list.html'
    context_object_name = 'viagens'

class ViagemDetailView(DetailView):
    model = Viagem
    template_name = 'notas/pages/viagem_detail.html'
    context_object_name = 'viagem'

class NotaListView(ListView):
    model = Nota
    template_name = 'notas/pages/nota_list.html'
    context_object_name = 'notas'

    def get_queryset(self):
        return Nota.objects.filter(viagem_id=self.kwargs['viagem_id'])

class ViagemCreateView(CreateView):
    model = Viagem
    form_class = ViagemForm
    template_name = 'notas/pages/viagem_form.html'
    success_url = reverse_lazy('viagem_list')

    def form_valid(self, form):
        if Viagem.objects.filter(status='Iniciada').exists():
            messages.error(self.request, 'Você já tem uma viagem iniciada. Finalize-a antes de iniciar uma nova.')
            return redirect('viagem_list')
        return super().form_valid(form)

class NotaCreateView(CreateView):
    model = Nota
    form_class = NotaForm
    template_name = 'notas/pages/nota_form.html'
    success_url = reverse_lazy('viagem_list')

    def get_initial(self):
        initial = super().get_initial()
        viagem_id = self.request.GET.get('viagem_id')
        if viagem_id:
            initial['viagem'] = get_object_or_404(Viagem, id=viagem_id, status='Iniciada')
        return initial

    def form_valid(self, form):
        viagem = form.cleaned_data['viagem']
        if viagem.status == 'Finalizada':
            messages.error(self.request, 'Não é possível adicionar notas a uma viagem finalizada.')
            return redirect('viagem_detail', pk=viagem.id)
        return super().form_valid(form)

    def form_valid(self, form):
        viagem = form.cleaned_data['viagem']
        if viagem.status == 'Finalizada':
            messages.error(self.request, 'Não é possível adicionar notas a uma viagem finalizada.')
            return redirect('viagem_detail', pk=viagem.id)
        return super().form_valid(form)

class FinalizarViagemView(View):
    def post(self, request, pk):
        viagem = Viagem.objects.get(pk=pk)
        viagem.status = 'Finalizada'
        viagem.data_fim = date.today()
        viagem.save()
        messages.success(request, 'Viagem finalizada com sucesso.')
        return redirect('viagem_detail', pk=pk)
