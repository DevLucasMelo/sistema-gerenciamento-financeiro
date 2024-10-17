from django.db import models
from django.contrib.auth.hashers import check_password

class Tipos_pagamentos(models.Model):
    tip_pag_id = models.AutoField(primary_key=True) 
    tip_pag_nome = models.CharField(max_length=255)
   
    class Meta:
        db_table = 'tipos_pagamentos'  

class Tipos_eletronicos(models.Model):
    tip_ele_id = models.AutoField(primary_key=True) 
    tip_ele_nome = models.CharField(max_length=255)
   
    class Meta:
        db_table = 'tipos_eletronicos' 

class Marcas(models.Model):
    mar_id = models.AutoField(primary_key=True) 
    mar_nome = models.CharField(max_length=255)
   
    class Meta:
        db_table = 'marcas' 

class Categorias(models.Model):
    cat_id = models.AutoField(primary_key=True) 
    cat_nome = models.CharField(max_length=255)
   
    class Meta:
        db_table = 'categorias' 

class Transacoes(models.Model):
    tra_id = models.AutoField(primary_key=True)  # Serial em PostgreSQL
    tra_cpf_cnpj = models.CharField(max_length=50)
    tra_tip_pag = models.ForeignKey(Tipos_pagamentos, on_delete=models.CASCADE, related_name='tipos_pagamentos')
    tra_valor = models.DecimalField(max_digits=10, decimal_places=2)
    tra_descricao = models.TextField()
    tra_tipo = models.CharField(max_length=100)
    tra_tip_ele = models.ForeignKey(Tipos_eletronicos, on_delete=models.CASCADE, related_name='tipos_eletronicos')
    tra_cat = models.ForeignKey(Categorias, on_delete=models.CASCADE, related_name='categorias')
    tra_modelo = models.CharField(max_length=255)
    tra_mar = models.ForeignKey(Marcas, on_delete=models.CASCADE, related_name='marcas')
    tra_data_criacao = models.DateField()
    tra_data_vencimento = models.DateField()
    tra_data_pagamento = models.DateField(null=True, blank=True)
    tra_data_cancelamento = models.DateField(null=True, blank=True)
    tra_pago = models.BooleanField(default=False)

    class Meta:
        db_table = 'transacoes'  # Define explicitamente o nome da tabela

class Usuarios(models.Model):
    usu_id = models.AutoField(primary_key=True)
    usu_nome = models.CharField(max_length=255)
    usu_cpf = models.CharField(max_length=20)
    usu_email = models.EmailField(max_length=255)
    usu_senha = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuarios'  

    def check_password(self, password):
        return check_password(password, self.usu_senha)
    
class Contas(models.Model):
    cts_id = models.AutoField(primary_key=True)
    cts_nome_titular_conta = models.CharField(max_length=255)
    cts_cpf_cnpj = models.CharField(max_length=50)
    cts_tipo_conta = models.CharField(max_length=50)
    cts_banco = models.CharField(max_length=50)
    cts_agencia = models.CharField(max_length=50)
    cts_num_conta_digito = models.CharField(max_length=50)
    cts_saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    cts_saldo_atual = models.DecimalField(max_digits=10, decimal_places=2)
    cts_data_criacao = models.DateTimeField() 

    class Meta:
        db_table = 'contas'  

class Enderecos(models.Model):

    end_id = models.AutoField(primary_key=True)
    end_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='enderecos')
    end_logradouro = models.CharField(max_length=255)
    end_numero = models.CharField(max_length=10)
    end_cidade = models.CharField(max_length=255)
    end_estado = models.CharField(max_length=10)
    end_cep = models.CharField(max_length=10)


    class Meta:
        db_table = 'enderecos'  


class OrdemServicos(models.Model):
    ord_ser_id = models.AutoField(primary_key=True)
    ord_ser_cli_nome = models.CharField(max_length=255)
    ord_ser_cli_cpf_cnpj = models.CharField(max_length=20)
    ord_ser_cli_telefone = models.CharField(max_length=20, blank=True)
    ord_ser_cli_email = models.EmailField(max_length=255, blank=True)
    ord_ser_cli_logradouro = models.TextField(blank=True)
    ord_ser_cli_numero = models.TextField(blank=True)
    ord_ser_cli_cidade = models.TextField(blank=True)
    ord_ser_cli_estado= models.TextField(blank=True)
    ord_ser_cli_cep = models.TextField(blank=True)
    ord_ser_numero = models.CharField(max_length=50, blank=True, unique=True)
    ord_ser_data_abertura = models.DateField(auto_now_add=True)
    ord_ser_data_prevista = models.DateField(null=True, blank=True)
    ord_ser_descricao = models.TextField(blank=True)
    ord_ser_categoria = models.CharField(max_length=100, blank=True)
    ord_ser_tecnico_responsavel = models.CharField(max_length=255, blank=True)
    ord_ser_itens_utilizados = models.TextField(blank=True)
    ord_ser_valor = models.DecimalField(max_digits=10, decimal_places=2)
    ord_ser_status = models.CharField(max_length=50, default='Em andamento')
    ord_ser_garantia = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'ordem_servicos'

