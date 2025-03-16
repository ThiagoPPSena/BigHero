from imbox import Imbox
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta, date
import re

class Email:
    def __init__(self):
        self.host = 'imap.gmail.com'
        self.email = 'thiagopinto.sena@gmail.com'
        self.password = 'upzo gmmg lect lnbt' 


    def get_last_code(self):
        with Imbox(self.host, username=self.email, password=self.password) as imbox:
            
            today = datetime.today().strftime("%d-%b-%Y")
            messages = imbox.messages(date__on=today)

            disney_emails = [] 

            for uid, message in messages:

                code = None
                
                subject = message.subject or ""
                email_content = ""

                if message.body['html']:
                    email_content = message.body['html'][0]  
                elif message.body['plain']:
                    email_content = message.body['plain'][0] 

                email_soup = bs(email_content, "html.parser")
                email_text = email_soup.get_text().strip()
                email_text = re.sub(r'\n+', '\n', email_text)  

                tds = email_soup.find_all("td")

                for td in tds:
                    content = td.text.strip()
                    
                    
                    if content.isdigit():
                        code = content

                if "disney" in subject.lower() or "disney" in email_text.lower():
                    disney_email = {
                        "assunto": subject,
                        "data": message.date,
                        "código": code
                    }
                    disney_emails.append(disney_email)

            if disney_emails:
                last_disney_email = disney_emails[-1]
                return last_disney_email 
            else:
                print("Nenhum e-mail da Disney encontrado nos últimos 30 min")


    def check_emails(self):
        now = datetime.now()
        past_minutes = now - timedelta(minutes=30)

        with Imbox(self.host, username=self.email, password=self.password) as imbox:
            
            messages = imbox.messages(date__gt=past_minutes)

            disney_emails = [] 

            for uid, message in messages:

                code = None
                # Pegando o assunto e o corpo do e-mail
                subject = message.subject or ""
                email_content = ""

                if message.body['html']:
                    email_content = message.body['html'][0]  # Pegando versão HTML
                elif message.body['plain']:
                    email_content = message.body['plain'][0]  # Pegando versão texto puro

                # Usando BeautifulSoup para limpar o HTML
                email_soup = bs(email_content, "html.parser")
                email_text = email_soup.get_text().strip()
                email_text = re.sub(r'\n+', '\n', email_text)  # Remover quebras de linha extras

                # Pegando todos os <td>s
                tds = email_soup.find_all("td")

                # Filtrando os <td>s que contêm uma string composta apenas por números
                for td in tds:
                    content = td.text.strip()
                    
                    # Verificando se o conteúdo é composto apenas por números (código numérico)
                    if content.isdigit():  # Verifica se a string contém apenas números
                        print(f'Código: {content}')
                        code = content

                # Verificando se "disney" está no assunto ou no corpo
                if "disney" in subject.lower() or "disney" in email_text.lower():
                    disney_email = {
                        "assunto": subject,
                        "data": message.date,
                        "código": code
                    }
                    disney_emails.append(disney_email)

            if disney_emails:
                last_disney_email = disney_emails[-1]
                return last_disney_email # Usando asyncio.run para chamar a função assíncrona
            else:
                print("Nenhum e-mail da Disney encontrado nos últimos 30 min")

email = Email()