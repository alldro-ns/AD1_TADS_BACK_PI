"""
Configuração principal de rotas do projeto SMC.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cadastros.urls')),
]
