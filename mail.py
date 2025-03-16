from imbox import Imbox
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import re
import os
from dotenv import load_dotenv
load_dotenv()

class Email:
    def __init__(self):
        self.host = os.getenv('MAIL_HOST')
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')

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

email = Email()