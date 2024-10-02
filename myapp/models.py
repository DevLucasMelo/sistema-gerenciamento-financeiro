from django.db import models
from django.contrib.auth.hashers import check_password


class Transacoes(models.Model):
    tra_id = models.AutoField(primary_key=True)  # Serial em PostgreSQL
    tra_cpf_cnpj = models.CharField(max_length=50)
    tra_metodo_pagamento = models.CharField(max_length=100)
    tra_valor = models.DecimalField(max_digits=10, decimal_places=2)
    tra_descricao = models.TextField()
    tra_tipo = models.CharField(max_length=100)
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