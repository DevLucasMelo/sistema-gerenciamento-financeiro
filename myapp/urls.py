from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('gerencia_financeiro/', views.gerencia_financeiro, name='gerencia_financeiro'),
    path('gerencia_contas/', views.gerencia_contas, name='gerencia_contas'),
    path('gerencia_usuarios/', views.gerencia_usuarios, name='gerencia_usuarios'),
    path('consulta_transacoes/', views.transacoes_view, name='consulta_transacoes'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('relatorio_financeiro/', views.relatorio_financeiro_view, name='relatorio_financeiro'),
    path('ordem_servico/', views.ordem_servico_view, name='ordem_servico'),
    path('gera_ordem_servico/', views.gera_ordem_servico_view, name='gera_ordem_servico'),
    path('consulta_ordem_servico/', views.consulta_ordem_servico_view, name='consulta_ordem_servico'),
    path('ordem_servico_template/<str:numero>/', views.imprime_ordem_servico_view, name='ordem_servico_template'),
    path('logout/', views.logout_view, name='logout'),
]
