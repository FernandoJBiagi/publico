from django import forms
from .models import Viagem, Nota

class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = ['data_inicio', 'data_fim', 'destino', 'veiculo', 'km_inicial', 'km_final', 'nome_funcionario', 'matricula', 'centro_de_custo', 'motivo']

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['tipo', 'valor_nota', 'data_nota', 'anexo', 'viagem']

    def __init__(self, *args, **kwargs):
        super(NotaForm, self).__init__(*args, **kwargs)
        self.fields['viagem'].queryset = Viagem.objects.filter(status='Iniciada')
