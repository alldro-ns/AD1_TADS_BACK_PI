from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Colaborador, RegistroHora
from .forms import ColaboradorForm, RegistroHoraForm


def login_view(request):
    """
    Tela de login para autenticação de administradores e consultores.
    """
    if request.user.is_authenticated:
        return redirect('home')

    mensagem_erro = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home')
        else:
            mensagem_erro = "Usuário ou senha inválidos. Por favor, tente novamente."
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
        'mensagem_erro': mensagem_erro
    })


def logout_view(request):
    """
    Encerra a sessão do usuário e redireciona para a página de login.
    """
    logout(request)
    return redirect('login')


@login_required
def home(request):
    """
    Página inicial do sistema SMC, com resumo geral e perfil do usuário logado.
    """
    total_colaboradores = Colaborador.objects.count()
    total_registros = RegistroHora.objects.count()

    return render(request, 'home.html', {
        'total_colaboradores': total_colaboradores,
        'total_registros': total_registros,
    })


@login_required
def lista_colaboradores(request):
    """
    Listagem de todos os colaboradores cadastrados.
    """
    colaboradores = Colaborador.objects.all().order_by('nome_completo')
    return render(request, 'lista_colaboradores.html', {
        'colaboradores': colaboradores
    })


@login_required
def cadastrar_colaborador(request):
    """
    Cadastro de um novo colaborador (Apenas Admin via interface).
    """
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_colaboradores')
    else:
        form = ColaboradorForm()

    return render(request, 'form_colaborador.html', {
        'form': form,
        'titulo': 'Cadastrar Novo Colaborador'
    })


@login_required
def editar_colaborador(request, id):
    """
    Edição dos dados de um colaborador existente.
    """
    colaborador = get_object_or_404(Colaborador, id=id)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            return redirect('lista_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)

    return render(request, 'form_colaborador.html', {
        'form': form,
        'titulo': f'Editar Colaborador: {colaborador.nome_completo}'
    })


@login_required
def excluir_colaborador(request, id):
    """
    Exclusão de um colaborador.
    """
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    return redirect('lista_colaboradores')


@login_required
def lista_horas(request):
    """
    Listagem de horas trabalhadas com diferenciação por perfil:
    - Admin (is_staff=True): vê todos os registros de todos os consultores.
    - Consultor (is_staff=False): vê apenas as suas próprias horas registradas.
    """
    if request.user.is_staff:
        horas = RegistroHora.objects.all().order_by('-data')
        tipo_visao = "Visão Geral de Administrador (Todos os Consultores)"
    else:
        horas = RegistroHora.objects.filter(colaborador__usuario=request.user).order_by('-data')
        tipo_visao = "Visão do Consultor (Apenas Minhas Horas)"

    # Soma simples das horas exibidas na lista atual (RF011)
    total_horas = sum(item.horas_trabalhadas for item in horas)

    return render(request, 'lista_horas.html', {
        'horas': horas,
        'total_horas': total_horas,
        'tipo_visao': tipo_visao,
    })


@login_required
def registrar_horas(request):
    """
    Lançamento de novo registro de horas trabalhadas.
    """
    if request.method == 'POST':
        form = RegistroHoraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_horas')
    else:
        # Se for consultor, pré-seleciona seu colaborador no formulário
        dados_iniciais = {}
        if not request.user.is_staff:
            colaborador_vinculado = Colaborador.objects.filter(usuario=request.user).first()
            if colaborador_vinculado:
                dados_iniciais['colaborador'] = colaborador_vinculado

        form = RegistroHoraForm(initial=dados_iniciais)

    return render(request, 'form_horas.html', {
        'form': form,
        'titulo': 'Registrar Atividade e Horas'
    })


@login_required
def editar_horas(request, id):
    """
    Edição de um apontamento de horas existente.
    """
    registro = get_object_or_404(RegistroHora, id=id)

    if request.method == 'POST':
        form = RegistroHoraForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('lista_horas')
    else:
        form = RegistroHoraForm(instance=registro)

    return render(request, 'form_horas.html', {
        'form': form,
        'titulo': f'Editar Horas: {registro.nome_projeto}'
    })


@login_required
def excluir_horas(request, id):
    """
    Exclusão de um apontamento de horas.
    """
    registro = get_object_or_404(RegistroHora, id=id)
    registro.delete()
    return redirect('lista_horas')
