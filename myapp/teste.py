from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

try:
    sg_api_key = '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' 
    sg = SendGridAPIClient(sg_api_key)
    message = Mail(
        from_email='meloeam1238@gmail.com',
        to_emails='faustinilucas8@gmail.com',
        subject='Relatório Financeiro com PDF',
        html_content='<strong>Segue o relatório financeiro em anexo.</strong>'
    )
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(f"Erro ao enviar email: {e}")
