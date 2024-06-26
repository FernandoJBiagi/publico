from django.urls import path
from .views import HomeView, ViagemListView, ViagemDetailView, NotaListView, ViagemCreateView, NotaCreateView, FinalizarViagemView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('viagens/', ViagemListView.as_view(), name='viagem_list'),
    path('viagens/<int:pk>/', ViagemDetailView.as_view(), name='viagem_detail'),
    path('viagens/<int:viagem_id>/notas/', NotaListView.as_view(), name='nota_list'),
    path('viagens/nova/', ViagemCreateView.as_view(), name='viagem_create'),
    path('notas/nova/', NotaCreateView.as_view(), name='nota_create'),
    path('viagens/<int:pk>/finalizar/', FinalizarViagemView.as_view(), name='finalizar_viagem'),
]
