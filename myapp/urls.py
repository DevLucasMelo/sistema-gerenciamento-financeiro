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
    path('logout/', views.logout_view, name='logout'),
]
