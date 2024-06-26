from django.db import models
from datetime import date

class Viagem(models.Model):
    STATUS_CHOICES = (
        ('Iniciada', 'Iniciada'),
        ('Finalizada', 'Finalizada'),
    )

    id = models.AutoField(primary_key=True)
    data_inicio = models.DateField(default=date.today)
    data_fim = models.DateField(null=True, blank=True)
    destino = models.CharField(max_length=100)
    veiculo = models.CharField(max_length=10)
    km_inicial = models.FloatField()
    km_final = models.FloatField(null=True, blank=True)
    nome_funcionario = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10)
    centro_de_custo = models.CharField(max_length=10)
    motivo = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Iniciada')

    def __str__(self):
        return f"Viagem para {self.destino} - {self.status}"

class Nota(models.Model):
    TIPO_ESCOLHAS = (
        ('AL', 'Alimentação'),
        ('CO', 'Combustível'),
        ('PE', 'Pedágio'),
        ('ES', 'Estacionamento'),
        ('NO', 'Nome'),
        ('HO', 'Hospedagem'),
        ('OU', 'Outros')
    )

    tipo = models.CharField(max_length=2, choices=TIPO_ESCOLHAS)
    valor_nota = models.FloatField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_nota = models.DateField(default=date.today)
    anexo = models.FileField(upload_to='attachments/', null=True, blank=True)
    viagem = models.ForeignKey(Viagem, on_delete=models.CASCADE, related_name='notas')

    def __str__(self):
        return f"Nota {self.id} - {self.tipo} - {self.valor_nota}"
