# SMC - Sistema de Medição de Contratos
**3Neuron Consultoria** | Trabalho Acadêmico (TADS - Back-end)

Aplicação web desenvolvida em **Python** e **Django** focada em **extrema simplicidade e didática**, voltada para apresentação em vídeo.

---

## 1. Requisitos
- Python 3.10 ou superior
- Django 5.0 ou superior

---

## 2. Instalação e Configuração

### Passo 1: Instalar dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Executar migrações do banco de dados
```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 3: Popular o banco com dados de teste
Execute o script de seed para criar usuários e registros de teste automaticamente:
```bash
python popular_banco.py
```

### Passo 4: Iniciar o servidor de desenvolvimento
```bash
python manage.py runserver
```
Acesse o sistema no navegador: `http://127.0.0.1:8000/`

---

## 3. Credenciais para Apresentação em Vídeo

| Perfil | Usuário | Senha | Acesso / Permissões |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | Acesso total: cria/edita/exclui colaboradores e vê todas as horas |
| **Consultor** | `consultor` | `consultor123` | Funcionário comum: apenas consulta colaboradores e vê suas próprias horas |

---

## 4. Estrutura do Projeto
- `smc/`: Configurações centrais do Django (`settings.py`, `urls.py`).
- `cadastros/`: App único da aplicação contendo:
  - `models.py`: Modelos `Colaborador` e `RegistroHora`.
  - `admin.py`: Customização do painel administrativo.
  - `forms.py`: Formulários `ColaboradorForm` e `RegistroHoraForm`.
  - `views.py`: Views baseadas em funções para regras de negócio e controle de perfis.
  - `templates/`: Templates HTML com Django Template Language e herança (`base.html`).
- `static/css/estilo.css`: Folha de estilo única em CSS puro, sem frameworks externos.
- `popular_banco.py`: Script de carga rápida de dados para testes.
