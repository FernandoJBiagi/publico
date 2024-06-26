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

    def form_invalid(self, form):
        return super().form_invalid(form)

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

class FinalizarViagemView(View):
    def post(self, request, pk):
        viagem = Viagem.objects.get(pk=pk)
        viagem.status = 'Finalizada'
        viagem.data_fim = date.today()
        viagem.save()
        messages.success(request, 'Viagem finalizada com sucesso.')
        return redirect('viagem_detail', pk=pk)

class CaixaListView(ListView):
    model = Viagem
    template_name = 'notas/pages/caixa_list.html'
    context_object_name = 'viagens'

    def get_queryset(self):
        return Viagem.objects.filter(status='Finalizada')

class NotaReviewView(View):
    template_name = 'notas/pages/nota_review.html'

    def get(self, request, *args, **kwargs):
        viagem_id = self.kwargs.get('viagem_id')
        viagem = get_object_or_404(Viagem, pk=viagem_id, status='Finalizada')
        notas = Nota.objects.filter(viagem=viagem)
        context = {
            'viagem': viagem,
            'notas': notas,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nota_id = request.POST.get('nota_id')
        nota = get_object_or_404(Nota, pk=nota_id)
        valor_nota = nota.valor_nota

        if valor_nota > 70:
            # Direcionar para dois aprovadores
            messages.success(request, 'Nota enviada para dois aprovadores.')
        else:
            # Direcionar para um aprovador
            messages.success(request, 'Nota enviada para um aprovador.')

        nota.status = 'Pendente'
        nota.save()

        return redirect('caixa_list')

class AprovadorListView(ListView):
    model = Nota
    template_name = 'notas/pages/aprovador_list.html'
    context_object_name = 'notas'

    def get_queryset(self):
        return Nota.objects.filter(status='Pendente')

class AprovarNotaView(View):
    def post(self, request, pk):
        nota = get_object_or_404(Nota, pk=pk)
        nota_status = request.POST.get('status')
        if nota_status == 'Aprovada':
            nota.status = 'Aprovada'
        elif nota_status == 'Reprovada':
            nota.status = 'Reprovada'
        nota.save()
        messages.success(request, 'Nota {} com sucesso.'.format(nota_status.lower()))
        return redirect('aprovador_list')
