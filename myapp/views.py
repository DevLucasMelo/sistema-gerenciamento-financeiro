import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import EmailMessage
from weasyprint import HTML, Attachment
from io import BytesIO
import random
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Usuarios, Contas, Enderecos, Transacoes, OrdemServicos
from django.db.models import Sum, Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .decorators import login_required 
from django.utils.timezone import now
from django.db.models.functions import TruncWeek, TruncMonth
import json
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

def index(request):
    return render(request, 'pagina_inicial.html')

@login_required
def gerencia_financeiro(request):
    return render(request, 'gerencia_financeiro.html')

@login_required
def gerencia_contas(request):
    if request.method == 'POST':
        cts_nome_titular_conta = request.POST['nome_titular']
        cts_cpf_cnpj = request.POST['cpf_cnpj']
        cts_tipo_conta = request.POST['tipo_conta']
        cts_banco = request.POST['banco']
        cts_agencia = request.POST['agencia']
        cts_num_conta_digito = request.POST['num_conta_digito']
        cts_saldo_inicial = request.POST['saldo_inicial']
        cts_saldo_atual = request.POST['saldo_atual']
        cts_data_criacao = datetime.now()


        conta = Contas(
            cts_nome_titular_conta=cts_nome_titular_conta,
            cts_cpf_cnpj=cts_cpf_cnpj,
            cts_tipo_conta=cts_tipo_conta,
            cts_banco=cts_banco,
            cts_agencia=cts_agencia,
            cts_num_conta_digito=cts_num_conta_digito,
            cts_saldo_inicial=cts_saldo_inicial,
            cts_saldo_atual=cts_saldo_atual,
            cts_data_criacao=cts_data_criacao
        )

        conta.save()

        return redirect('gerencia_contas')

    return render(request, 'gerencia_contas.html')

@login_required
def gerencia_usuarios(request):
    if request.method == 'POST':
        
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        email = request.POST['email']
        
        
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        cep = request.POST['cep']
        
        
        usuario = Usuarios(
            usu_nome=nome,
            usu_cpf=cpf,
            usu_email=email
        )
        usuario.save()
        
        
        endereco = Enderecos(
            end_logradouro=logradouro,
            end_numero=numero,
            end_cidade=cidade,
            end_estado=estado,
            end_cep=cep,
            end_usu_id=usuario.usu_id  
        )
        endereco.save()
        
        return redirect('gerencia_usuarios')

    return render(request, 'gerencia_usuarios.html')

def login_view(request):
    if request.method == 'POST':
        usu_email = request.POST['email']
        senha = request.POST['senha']
        
        try:
            usuario = Usuarios.objects.get(usu_email=usu_email)
            if usuario.check_password(senha):
                
                request.session['usuario_id'] = usuario.usu_id
                request.session.set_expiry(24 * 60 * 60) 
                return redirect('gerencia_financeiro')  
            else:
                return render(request, 'login.html', {'erro': 'Senha incorreta.'})

        except ObjectDoesNotExist:
            
            return render(request, 'login.html', {'erro': 'Usuário não foi encontrado.'})
        except MultipleObjectsReturned:
            
            return render(request, 'login.html', {'erro': 'Erro: múltiplos usuários com o mesmo email.'})
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required
def transacoes_view(request):
    tipo_filtro = request.GET.get('tipo', '')

    
    if tipo_filtro:
        transacoes = Transacoes.objects.filter(tra_tipo=tipo_filtro).prefetch_related('tra_tip_pag', 'tra_tip_ele', 'tra_cat', 'tra_mar')
    else:
        transacoes = Transacoes.objects.all().prefetch_related('tra_tip_pag', 'tra_tip_ele', 'tra_cat', 'tra_mar')


    paginator = Paginator(transacoes, 20)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    
    total_valor = transacoes.aggregate(total=Sum('tra_valor'))['total'] or 0

    
    return render(request, 'consulta_transacoes.html', {
        'transacoes': page_obj,  
        'total_valor': total_valor,
        'page_obj': page_obj  
    })

@login_required
def dashboard_view(request):
    transacoes = Transacoes.objects.all()

    
    receitas = transacoes.filter(tra_tipo='Contas a Receber').aggregate(total_receitas=Sum('tra_valor'))['total_receitas'] or 0
    despesas = transacoes.filter(tra_tipo='Contas a Pagar').aggregate(total_despesas=Sum('tra_valor'))['total_despesas'] or 0
    lucro_liquido = receitas - despesas

    
    hoje = now().date()
    inicio_do_ano = hoje.replace(month=1, day=1)  

    
    quatro_semanas_atras = datetime.now() - timedelta(weeks=4)

    
    transacoes_semanal = (
        Transacoes.objects
        .filter(tra_data_vencimento__gte=quatro_semanas_atras)
        .annotate(semana=TruncWeek('tra_data_vencimento'))  
        .values('semana')  
        .annotate(total_receitas=Sum('tra_valor', filter=Q(tra_tipo='Contas a Receber')), 
                  total_despesas=Sum('tra_valor', filter=Q(tra_tipo='Contas a Pagar')))  
    )

    
    semanas = []
    valores_receitas = []
    valores_despesas = []

    for transacao in transacoes_semanal:
        semanas.append(transacao['semana'].strftime('%Y-%m-%d'))  
        valores_receitas.append(float(transacao['total_receitas'] or 0))  
        valores_despesas.append(float(transacao['total_despesas'] or 0))  

    
    tres_meses_atras = datetime.now() - relativedelta(months=3)

    
    transacoes_mensal = (
        Transacoes.objects
        .filter(tra_data_vencimento__gte=tres_meses_atras)
        .annotate(mes=TruncMonth('tra_data_vencimento'))  
        .values('mes')  
        .annotate(total_receitas=Sum('tra_valor', filter=Q(tra_tipo='Contas a Receber')), 
                  total_despesas=Sum('tra_valor', filter=Q(tra_tipo='Contas a Pagar')))  
    )

    
    meses = []
    valores_receitas_mensal = []
    valores_despesas_mensal = []

    for transacao in transacoes_mensal:
        meses.append(transacao['mes'].strftime('%Y-%m'))  
        valores_receitas_mensal.append(float(transacao['total_receitas'] or 0))  
        valores_despesas_mensal.append(float(transacao['total_despesas'] or 0))  

    
    receitas_anual = float(transacoes.filter(tra_tipo='Contas a Receber', tra_data_vencimento__gte=inicio_do_ano).aggregate(total_receitas=Sum('tra_valor'))['total_receitas'] or 0)
    despesas_anual = float(transacoes.filter(tra_tipo='Contas a Pagar', tra_data_vencimento__gte=inicio_do_ano).aggregate(total_despesas=Sum('tra_valor'))['total_despesas'] or 0)

    lucro_liquido = receitas_anual - despesas_anual
    
    context = {
        'semanas': semanas,
        'valores_receitas': valores_receitas,
        'valores_despesas': valores_despesas,
        'meses': meses,
        'valores_receitas_mensal': valores_receitas_mensal,
        'valores_despesas_mensal': valores_despesas_mensal,
        'lucro_liquido_semanal': [valores_receitas[i] - valores_despesas[i] for i in range(len(valores_receitas))],
        'lucro_liquido_mensal': [valores_receitas_mensal[i] - valores_despesas_mensal[i] for i in range(len(valores_receitas_mensal))],
        'receitas_anual': receitas_anual,
        'despesas_anual': despesas_anual,
        'lucro_liquido': lucro_liquido,
    }

    return render(request, 'dashboard.html', context)

def enviar_email_com_pdf(caminho_pdf, data_inicio, data_fim, email):
    
    with open(caminho_pdf, 'rb') as f:
        dados_pdf = f.read()

    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
    data_fim = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')


    
    encoded_pdf = base64.b64encode(dados_pdf).decode()
    print(email)
    print(email)
    message = Mail(
        from_email='meloeam1238@gmail.com',
        to_emails=f'{email}',
        subject=f'Relatório Financeiro no perído de {data_inicio} até {data_fim}',
        html_content='<strong>Segue o relatório financeiro em anexo.</strong>'
    )

    
    anexo = Attachment()
    anexo.file_content = FileContent(encoded_pdf)
    anexo.file_type = FileType('application/pdf')
    anexo.file_name = FileName('relatorio_financeiro.pdf')
    anexo.disposition = Disposition('attachment')

    
    message.attachment = anexo

    
    try:
        load_dotenv()
        sg_api_key = os.getenv('SENDGRID_API_KEY')
        sg = SendGridAPIClient(sg_api_key)
        response = sg.send(message)
        print('enviou')
    except Exception as e:
        print(e)


@login_required
def relatorio_financeiro_view(request):
    if request.method == 'POST':
        data_inicio = request.POST.get('startDate')
        data_fim = request.POST.get('endDate')
        email = request.POST.get('email')

        if data_inicio and data_fim and email:

            transacoes = Transacoes.objects.filter(tra_data_vencimento__range=[data_inicio, data_fim])
            
            total_receber = sum(transacao.tra_valor for transacao in transacoes if transacao.tra_tipo == 'Contas a Receber')
            total_pagar = sum(transacao.tra_valor for transacao in transacoes if transacao.tra_tipo == 'Contas a Pagar')

            lucro_liquido = total_receber - total_pagar
            
            data_inicio_formatada = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
            data_fim_formatada = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d/%m/%Y')

            
            html_string = render_to_string('relatorio_pdf_template.html', {'transacoes': transacoes, 'total_receber': total_receber, 'total_pagar':total_pagar, 'lucro_liquido': lucro_liquido, 'data_inicio_formatada': data_inicio_formatada, 'data_fim_formatada': data_fim_formatada})
            
            
            caminho_relatorios = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'relatorios')
            if not os.path.exists(caminho_relatorios):
                os.makedirs(caminho_relatorios)  

            caminho_pdf = os.path.join(caminho_relatorios, f'relatorio_{data_inicio}_a_{data_fim}.pdf')

            
            HTML(string=html_string).write_pdf(caminho_pdf)

            
            enviar_email_com_pdf(caminho_pdf, data_inicio, data_fim, email)
            
            return render(request, 'relatorio_financeiro.html', {'success': True})

            
    return render(request, 'relatorio_financeiro.html')

@login_required
def ordem_servico_view(request):
    
    return render(request, 'ordem_servico.html')

@login_required
def gera_ordem_servico_view(request):

    if request.method == 'POST':
        ord_ser_cli_nome = request.POST['ord_ser_cli_nome']
        ord_ser_cli_cpf_cnpj = request.POST['ord_ser_cli_cpf_cnpj']
        ord_ser_cli_email = request.POST['ord_ser_cli_email']
        ord_ser_cli_telefone = request.POST['ord_ser_cli_telefone']
        ord_ser_data_abertura = request.POST['ord_ser_data_abertura']
        ord_ser_data_prevista = request.POST['ord_ser_data_prevista']
        ord_ser_descricao = request.POST['ord_ser_descricao']
        ord_ser_categoria = request.POST['ord_ser_categoria']
        ord_ser_tecnico_responsavel = request.POST['ord_ser_tecnico_responsavel']
        ord_ser_itens_utilizados = request.POST['ord_ser_itens_utilizados']
        ord_ser_valor = request.POST['ord_ser_valor']
        ord_ser_status = request.POST['ord_ser_status']
        ord_ser_garantia = request.POST['ord_ser_garantia']
        ord_ser_cli_logradouro = request.POST['ord_ser_cli_logradouro']
        ord_ser_cli_numero = request.POST['ord_ser_cli_numero']
        ord_ser_cli_cidade = request.POST['ord_ser_cli_cidade']
        ord_ser_cli_estado = request.POST['ord_ser_cli_estado']
        ord_ser_cli_cep = request.POST['ord_ser_cli_cep']
        
        def gerar_numero_unico():
            while True:
                numero = str(random.randint(100000000000, 999999999999))
                if not OrdemServicos.objects.filter(ord_ser_numero=numero).exists():
                    return numero
                
        ord_ser_numero = gerar_numero_unico()

         
        ordem_servicos = OrdemServicos(
            ord_ser_cli_nome = ord_ser_cli_nome,
            ord_ser_cli_cpf_cnpj = ord_ser_cli_cpf_cnpj,
            ord_ser_cli_email = ord_ser_cli_email,
            ord_ser_cli_telefone = ord_ser_cli_telefone,
            ord_ser_cli_logradouro = ord_ser_cli_logradouro,
            ord_ser_cli_numero = ord_ser_cli_numero,
            ord_ser_cli_cidade = ord_ser_cli_cidade,
            ord_ser_cli_estado = ord_ser_cli_estado,
            ord_ser_cli_cep = ord_ser_cli_cep,
            ord_ser_numero = ord_ser_numero, 
            ord_ser_data_abertura = ord_ser_data_abertura, 
            ord_ser_data_prevista = ord_ser_data_prevista,
            ord_ser_descricao = ord_ser_descricao,
            ord_ser_categoria = ord_ser_categoria,
            ord_ser_tecnico_responsavel = ord_ser_tecnico_responsavel, 
            ord_ser_itens_utilizados = ord_ser_itens_utilizados,
            ord_ser_valor = ord_ser_valor,
            ord_ser_status = ord_ser_status,
            ord_ser_garantia = ord_ser_garantia
        )
        ordem_servicos.save()
                
        return redirect('consulta_ordem_servico')

    return render(request, 'gera_ordem_servico.html')

@login_required
def consulta_ordem_servico_view(request):
    ordemServicos = OrdemServicos.objects.only()

    return render(request, 'consulta_ordem_servico.html', {'ordemServicos': ordemServicos})
    
def imprime_ordem_servico_view(request, numero):

    ordem_servico = get_object_or_404(OrdemServicos, ord_ser_numero=numero)
    print(ordem_servico)
    return render(request, 'ordem_servico_template.html', {'ordem_servico': ordem_servico})