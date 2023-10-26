import os
import sys

# Configura el entorno de Django
# Configura el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cBankMain.settings")
import django
django.setup()

# Ahora puedes importar tus modelos
from dashboard.models import BankAccount, Contacto, Withdrawal, WithdrawalAccount, WithdrawalRequest


import sys
#print("sys->",sys.executable)
import base64
import email
import re
import schedule
import time
from googleapiclient.http import MediaIoBaseUpload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Google import Create_Service
from datetime import datetime
from email.utils import parsedate_to_datetime
import os
import sys
from dashboard import models

users=models.User.objects.all()



def main():
    cuentas_aprobadas = BankAccount.objects.filter(active=True)
    
    if cuentas_aprobadas.exists():
        print("Cuentas Aprobadas:")
        for cuenta in cuentas_aprobadas:
            print(f"Nombre del Titular: {cuenta.etiqueta}")
            print(f"estado Actual: {cuenta.active}")
            # Agrega aquí otros campos que quieras mostrar
            print("-" * 30)
    else:
        print("No se encontraron cuentas aprobadas.")

# Llama a la función para mostrar las cuentas aprobadas



class EmailProcessor:
    def __init__(self):
        self.gmail_service = self.construct_service("gmail")

    def construct_service(self, api_service):
        try:
            if api_service == "gmail":
                CLIENT_SERVICE_FILE = "credentials.json"
                API_NAME = "gmail"
                API_VERSION = "v1"
                SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
                return Create_Service(CLIENT_SERVICE_FILE, API_NAME, API_VERSION, SCOPES)
        except Exception as e:
            print(e)
            return None

    def search_email(self, query_string, label_ids=[]):
        try:
            message_list_response = (
                self.gmail_service.users()
                .messages()
                .list(userId="me", labelIds=label_ids, q=query_string)
                .execute()
            )

            message_items = message_list_response.get("messages")
            nextPageToken = message_list_response.get("nextPageToken")

            while nextPageToken:
                message_list_response = (
                    self.gmail_service.users()
                    .messages()
                    .list(
                        userId="me",
                        labelIds=label_ids,
                        q=query_string,
                        pageToken=nextPageToken,
                    )
                    .execute()
                )

                message_items.extend(message_list_response.get("messages"))
                nextPageToken = message_list_response.get("nextPageToken")
            return message_items

        except Exception as e:
            print(e)
            return []

    def get_message_detail(self, message_id):
        try:
            message = (
                self.gmail_service.users()
                .messages()
                .get(userId="me", id=message_id, format="raw")
                .execute()
            )

            message_data = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
            mime_msg = email.message_from_bytes(message_data)

            print(f"From: {mime_msg['From']}")
            print(f"To: {mime_msg['To']}")
            print(f"Subject: {mime_msg['Subject']}")
            print("models users: ",users)
            # Obtener la fecha como objeto datetime
            received_date = parsedate_to_datetime(mime_msg['Date'])
            # Formatear la fecha en el formato deseado
            formatted_date = received_date.strftime("%a, %d %b %Y %H:%M:%S %z")
            print(f"Date: {formatted_date}")

            if mime_msg.is_multipart():
                for part in mime_msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        print("Todo el texto ->", part.get_payload())
                        texto_email = part.get_payload()
                    elif content_type == "text/html":
                        pass
                        # print(f"\nHTML Body:\n{part.get_payload()}\n")
            else:
                content_type = mime_msg.get_content_type()
                if content_type == "text/plain":
                    pass
                    # print(mime_msg.get_payload())
                elif content_type == "text/html":
                    pass
                    # print(f"\nHTML Body:\n{mime_msg.get_payload()}\n")

            return texto_email, received_date

        except Exception as e:
            print(e)
            return None, None
    
    def parse_email(self, email_data):
        try:
            email_text, received_date = email_data

            # Buscar etiqueta en el texto del correo electrónico
            tag_regex = re.compile(r"Etiqueta cliente recibe el pago\s*-->\s*(.*)")
            tag_match = tag_regex.search(email_text)
            tag1 = tag_match.group(1).strip() if tag_match else None

            # Obtener nombre de quien envía el correo
            name_regex = re.compile(r"From:\s*=\?UTF-8\?B\?(.*?)\?=")
            name_match = name_regex.search(email_text)
            name1 = name_match.group(1).strip() if name_match else None

            # Obtener cantidad del pago
            amount_regex = re.compile(r"Todo el texto\s*->\s*pago zeller (\d+\.\d+)")
            amount_match = amount_regex.search(email_text)
            amount1 = amount_match.group(1).strip() if amount_match else None

            return tag1, name1, amount1, received_date

        except Exception as e:
            print(e)
            return None, None, None, None
    
    def process_emails(self):
        # Filtro de búsqueda por el remitente
        query_string = "from:alistdk@gmail.com"

        # Obtener lista de mensajes que cumplen con el filtro de búsqueda
        email_resultados = self.search_email(query_string, ["INBOX"])

        for mensaje in email_resultados:
            mensaje_id = mensaje["id"]
            mensaje_detalle = self.get_message_detail(mensaje_id)
            tag1, name1, amount1, received_date = self.parse_email(mensaje_detalle)
            print("Etiqueta cliente recibe el pago -->", tag1)
            print("Nombre de quien envía -->", name1)
            print("Cantidad del pago -->", amount1)
            print("Fecha de recepción -->", received_date.strftime("%a, %d %b %Y %H:%M:%S %z"))
            print("############-------------------############# ")

    def run(self):
        # Ejecutar la verificación de correo cada 1 minuto
        schedule.every(1).minutes.do(self.process_emails)

        while True:
            schedule.run_pending()
            time.sleep(5)



if __name__ == "__main__":
    email_processor = EmailProcessor()
    email_processor.run()
    main()