from django.urls import path
from . import views

urlpatterns = [
    # Página inicial e Autenticação
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Gestão de Colaboradores (RF001)
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
    path('colaboradores/novo/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('colaboradores/editar/<int:id>/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),

    # Gestão e Apontamento de Horas (RF010, RF011, RF017)
    path('horas/', views.lista_horas, name='lista_horas'),
    path('horas/registrar/', views.registrar_horas, name='registrar_horas'),
    path('horas/editar/<int:id>/', views.editar_horas, name='editar_horas'),
    path('horas/excluir/<int:id>/', views.excluir_horas, name='excluir_horas'),
    path('horas/aprovar/<int:id>/', views.aprovar_hora, name='aprovar_hora'),
]
