from django.urls import path
from .views import HomeView, ViagemListView, ViagemDetailView, NotaListView, ViagemCreateView, NotaCreateView, FinalizarViagemView, CaixaListView, NotaReviewView, AprovadorListView, AprovarNotaView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('viagens/', ViagemListView.as_view(), name='viagem_list'),
    path('viagens/<int:pk>/', ViagemDetailView.as_view(), name='viagem_detail'),
    path('viagens/<int:viagem_id>/notas/', NotaListView.as_view(), name='nota_list'),
    path('viagens/nova/', ViagemCreateView.as_view(), name='viagem_create'),
    path('notas/nova/', NotaCreateView.as_view(), name='nota_create'),
    path('viagens/<int:pk>/finalizar/', FinalizarViagemView.as_view(), name='finalizar_viagem'),
    path('caixa/', CaixaListView.as_view(), name='caixa_list'),
    path('caixa/nota/<int:viagem_id>/', NotaReviewView.as_view(), name='nota_review'),
    path('aprovador/', AprovadorListView.as_view(), name='aprovador_list'),
    path('aprovar/nota/<int:pk>/', AprovarNotaView.as_view(), name='aprovar_nota'),
]
