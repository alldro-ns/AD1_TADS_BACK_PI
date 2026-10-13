from django import forms
from .models import Colaborador, RegistroHora


class ColaboradorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de colaboradores.
    """
    class Meta:
        model = Colaborador
        fields = [
            'usuario',
            'nome_completo',
            'cpf',
            'email',
            'cargo',
            'tipo_contratacao',
            'perfil',
        ]


class RegistroHoraForm(forms.ModelForm):
    """
    Formulário para apontamento e edição de horas trabalhadas.
    """
    class Meta:
        model = RegistroHora
        fields = [
            'colaborador',
            'nome_projeto',
            'data',
            'horas_trabalhadas',
            'descricao_atividade',
            'status',
        ]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
