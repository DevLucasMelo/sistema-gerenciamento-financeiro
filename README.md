O objetivo desse sistema Web é desenvolver um sistema de gerenciamento financeiro de uma loja de manutenções de eletrônicos (Computadores, celulares, tablets e notebooks) 
capaz de enviar relatórios financeiros baseado em transações cadastradas no banco dedados, gerenciar usuarios e contas, 
consultar transações com filtros específicos, consultar dashboards em tempo real feitos com os dados que estão no BD e com a ferramenta Metabase (Bussiness Inteligence). 

Tecnologias utilizadas no projeto:

- Python
- Django
- PostgreSQL 15
- Docker
- Metabase (Dashboards com dados ficticios do banco de dados)
- Html, CSS e Bootstrap
- Render (Hospedagem da aplicação gratuitamente)

Para executar o projeto será necessário utilizar o docker:

- Abra a pasta do projeto no editor de códigos e através do terminal execute os seguintes comandos:
  
1. docker-compose build

2. docker-compose up

3. Acessar o projeto no navegador através da URL: http://localhost:8000/

4. Clique em "Realizar login"

5. Utilize o e-mail: maria.silva@email.com e senha: senha123

6. Teste as funcionalidades da aplicação 


Principais dependências:


- Weasyprint
- Gunicorn
- WhiteNoise
