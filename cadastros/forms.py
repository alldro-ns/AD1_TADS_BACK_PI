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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exibe apenas contas de usuário que ainda não estão vinculadas a nenhum colaborador
        usuarios_ocupados = Colaborador.objects.filter(usuario__isnull=False)
        if self.instance and self.instance.pk:
            usuarios_ocupados = usuarios_ocupados.exclude(pk=self.instance.pk)

        self.fields['usuario'].queryset = User.objects.exclude(
            id__in=usuarios_ocupados.values_list('usuario_id', flat=True)
        )
        self.fields['usuario'].empty_label = "--- Nenhum (Colaborador sem acesso ao sistema) ---"
        self.fields['usuario'].required = False
        self.fields['usuario'].help_text = (
            "Opcional. Selecione um usuário do sistema para login ou deixe em branco se não possuir login."
        )


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
