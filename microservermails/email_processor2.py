import os
import sys
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
#from dashboard.models import Email_Data

Email_Data=""

class EmailProcessor:
    def __init__(self):
        self.gmail_service = self.construct_service("gmail")
        self.last_records = []

    def construct_service(self, api_service):
        try:
            if api_service == "gmail":
                CLIENT_SERVICE_FILE = os.path.join(project_path, "credentials.json")
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

            # Obtener la fecha como objeto datetime
            received_date = parsedate_to_datetime(mime_msg['Date'])
            # Formatear la fecha en el formato deseado
            formatted_date = received_date.strftime("%a, %d %b %Y %H:%M:%S %z")
            print(f"Date: {formatted_date}")

            texto_email = ""  # Establecer un valor predeterminado

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

            # Buscar etiquetas en el texto del correo
            tag_regex = re.compile(r"\*([^\n]+)\n")
            tag_match = tag_regex.search(email_text)
            if tag_match:
                tag1 = tag_match.group(1)
            else:
                tag1 = None

            # Buscar nombre en el texto del correo y la cantidad
            name_regex = re.compile(r"([A-Za-z]+ [A-Za-z]+) (le ha enviado|le envi=C3=B3) \$(\d+\.\d{2})")
            name_match = name_regex.search(email_text)
            if name_match:
                name1 = name_match.group(1)
                amount1 = float(name_match.group(3))
            else:
                name1 = None
                amount1 = None

            # Verificar si el registro ya existe en la lista de los últimos registros agregados
            existing_record = next((record for record in self.last_records if record['etiqueta'] == tag1 and record['nombre'] == name1 and record['cantidad'] == amount1), None)

            if existing_record:
                # Registro existente encontrado, no se agrega nuevamente
                return None, None, None, None

            # Crear una instancia del modelo Email y guardarla en la base de datos
            email = Email_Data(etiqueta=tag1, nombre=name1, cantidad=amount1, fecha=received_date)
            email.save()

            # Agregar el registro a la lista de los últimos registros agregados
            self.last_records.append({'etiqueta': tag1, 'nombre': name1, 'cantidad': amount1})

            # Limitar la lista a un número máximo de registros, si es necesario
            max_records = 100  # Define el número máximo de registros a retener
            if len(self.last_records) > max_records:
                self.last_records = self.last_records[-max_records:]

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
            print("Nombre de quien envia -->", name1)
            print("Cantidad del pago -->", amount1)
            if received_date is not None:
                print("Fecha de recepcion -->", received_date.strftime("%a, %d %b %Y %H:%M:%S %z"))
            else:
                print("Fecha de recepción no disponible")
            print("############-------------------############# ")

    def run(self):
        # Ejecutar la verificación de correo cada 1 minuto
        schedule.every(1).minutes.do(self.process_emails)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    # Agrega la ruta del proyecto al sys.path
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cBankMain'))
    sys.path.append(project_path)

    # Configura la variable de entorno DJANGO_SETTINGS_MODULE
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cBankMain.settings'

    import django
    django.setup()

    email_processor = EmailProcessor()
    email_processor.run()
