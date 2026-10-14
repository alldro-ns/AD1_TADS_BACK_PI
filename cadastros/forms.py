from django import forms
from django.contrib.auth.models import User
from .models import Colaborador, RegistroHora


class ColaboradorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de colaboradores e seus respectivos
    usuários de login (RF001).
    """
    nome_usuario = forms.CharField(
        label="Nome de Usuário (Login)",
        max_length=150,
        help_text="Identificador único para o colaborador entrar no sistema."
    )
    senha = forms.CharField(
        label="Senha de Acesso",
        widget=forms.PasswordInput,
        required=False,
        help_text="Defina a senha inicial (na edição, deixe em branco para manter a senha atual)."
    )

    class Meta:
        model = Colaborador
        fields = [
            'nome_completo',
            'cpf',
            'email',
            'cargo',
            'tipo_contratacao',
            'perfil',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se for edição e já tiver usuário vinculado, preenche o campo nome_usuario
        if self.instance and self.instance.pk and self.instance.usuario:
            self.fields['nome_usuario'].initial = self.instance.usuario.username
        else:
            # No novo cadastro, a senha é obrigatória
            self.fields['senha'].required = True

    def clean_nome_usuario(self):
        nome_usuario = self.cleaned_data.get('nome_usuario')
        usuario_atual = self.instance.usuario if (self.instance and self.instance.pk) else None

        # Garante que o username seja único no Django auth_user
        qs = User.objects.filter(username=nome_usuario)
        if usuario_atual:
            qs = qs.exclude(pk=usuario_atual.pk)
        if qs.exists():
            raise forms.ValidationError("Este nome de usuário já está em uso no sistema. Escolha outro.")
        return nome_usuario

    def save(self, commit=True):
        colaborador = super().save(commit=False)
        nome_usuario = self.cleaned_data.get('nome_usuario')
        senha = self.cleaned_data.get('senha')
        is_admin = (colaborador.perfil == 'ADM')

        if colaborador.usuario:
            # Atualiza a conta de login existente
            usuario = colaborador.usuario
            usuario.username = nome_usuario
            if senha:
                usuario.set_password(senha)
            usuario.is_staff = is_admin
            usuario.is_superuser = is_admin
            usuario.email = colaborador.email
            usuario.save()
        else:
            # Cria a conta de login no Django e vincula ao colaborador
            usuario = User.objects.create_user(
                username=nome_usuario,
                password=senha,
                email=colaborador.email,
                is_staff=is_admin,
                is_superuser=is_admin
            )
            colaborador.usuario = usuario

        if commit:
            colaborador.save()
        return colaborador


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
