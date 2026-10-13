from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from .models import Colaborador, RegistroHora


class SMCTests(TestCase):
    def setUp(self):
        # Usuário Administrador
        self.user_admin = User.objects.create_user(
            username='admin_teste',
            password='senha123',
            is_staff=True,
            is_superuser=True
        )
        self.colab_admin = Colaborador.objects.create(
            usuario=self.user_admin,
            nome_completo='Gestor Admin',
            cpf='111.111.111-11',
            email='admin@teste.com',
            cargo='Gerente',
            tipo_contratacao='CLT',
            perfil='ADM'
        )

        # Usuário Consultor
        self.user_consultor = User.objects.create_user(
            username='consultor_teste',
            password='senha123',
            is_staff=False
        )
        self.colab_consultor = Colaborador.objects.create(
            usuario=self.user_consultor,
            nome_completo='Consultor Teste',
            cpf='222.222.222-22',
            email='consultor@teste.com',
            cargo='Consultor',
            tipo_contratacao='PJ',
            perfil='CON'
        )

        # Registros de horas
        self.hora1 = RegistroHora.objects.create(
            colaborador=self.colab_consultor,
            nome_projeto='Projeto A',
            data=date(2026, 10, 1),
            horas_trabalhadas=Decimal('8.0'),
            descricao_atividade='Atividade do consultor',
            status='APR'
        )
        self.hora2 = RegistroHora.objects.create(
            colaborador=self.colab_admin,
            nome_projeto='Projeto B',
            data=date(2026, 10, 2),
            horas_trabalhadas=Decimal('4.0'),
            descricao_atividade='Atividade do admin',
            status='PEN'
        )

        self.client = Client()

    def test_str_dos_modelos(self):
        self.assertEqual(str(self.colab_admin), 'Gestor Admin')
        self.assertEqual(str(self.hora1), f"Consultor Teste - Projeto A ({date(2026, 10, 1)})")

    def test_login_e_redirecionamento(self):
        resposta = self.client.post(reverse('login'), {
            'username': 'admin_teste',
            'password': 'senha123'
        })
        self.assertRedirects(resposta, reverse('home'))

    def test_visao_horas_admin_ve_tudo(self):
        self.client.login(username='admin_teste', password='senha123')
        resposta = self.client.get(reverse('lista_horas'))
        self.assertEqual(resposta.status_code, 200)
        # Admin vê os 2 registros
        self.assertEqual(len(resposta.context['horas']), 2)
        # Total de horas: 8.0 + 4.0 = 12.0
        self.assertEqual(resposta.context['total_horas'], Decimal('12.0'))
        self.assertIn("Visão Geral de Administrador", resposta.context['tipo_visao'])

    def test_visao_horas_consultor_ve_apenas_as_suas(self):
        self.client.login(username='consultor_teste', password='senha123')
        resposta = self.client.get(reverse('lista_horas'))
        self.assertEqual(resposta.status_code, 200)
        # Consultor vê apenas o seu registro
        self.assertEqual(len(resposta.context['horas']), 1)
        self.assertEqual(resposta.context['total_horas'], Decimal('8.0'))
        self.assertIn("Visão do Consultor", resposta.context['tipo_visao'])

    def test_lista_colaboradores_renderiza(self):
        self.client.login(username='admin_teste', password='senha123')
        resposta = self.client.get(reverse('lista_colaboradores'))
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.context['colaboradores']), 2)

    def test_cadastrar_horas(self):
        self.client.login(username='consultor_teste', password='senha123')
        resposta = self.client.post(reverse('registrar_horas'), {
            'colaborador': self.colab_consultor.id,
            'nome_projeto': 'Projeto Novo',
            'data': '2026-10-05',
            'horas_trabalhadas': '6.0',
            'descricao_atividade': 'Nova atividade',
            'status': 'PEN'
        })
        self.assertRedirects(resposta, reverse('lista_horas'))
        self.assertTrue(RegistroHora.objects.filter(nome_projeto='Projeto Novo').exists())
