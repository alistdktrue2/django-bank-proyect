import base64
import email
import re
from datetime import time
from googleapiclient.http import MediaIoBaseUpload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import re
from Google import Create_Service


# Constantes
CLIENT_SERVICE_FILE = "credentials.json"
API_SERVICE_GMAIL = "gmail"
API_SERVICE_DRIVE = "drive"
API_VERSION_GMAIL = "v1"
API_VERSION_DRIVE = "v3"
SCOPES_GMAIL = ["https://www.googleapis.com/auth/gmail.readonly"]
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive"]


def construct_service(api_service):
    try:
        if api_service == API_SERVICE_DRIVE:
            return Create_Service(CLIENT_SERVICE_FILE, API_SERVICE_DRIVE, API_VERSION_DRIVE, SCOPES_DRIVE)
        elif api_service == API_SERVICE_GMAIL:
            return Create_Service(CLIENT_SERVICE_FILE, API_SERVICE_GMAIL, API_VERSION_GMAIL, SCOPES_GMAIL)
    except Exception as e:
        print(e)
        return None


def search_email(service, query_string, label_ids=[]):
    try:
        message_list_response = (
            service.users()
            .messages()
            .list(userId="me", labelIds=label_ids, q=query_string)
            .execute()
        )

        message_items = message_list_response.get("messages")
        nextPageToken = message_list_response.get("nextPageToken")

        while nextPageToken:
            message_list_response = (
                message_list_response.get("messages")
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


def get_message_detail(service, message_id):
    try:
        message = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="raw")
            .execute()
        )

        message_data = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
        mime_msg = email.message_from_bytes(message_data)

        print(f"From: {mime_msg['From']}")
        print(f"To: {mime_msg['To']}")
        print(f"Subject: {mime_msg['Subject']}")
        print(f"Date: {mime_msg['Date']}")

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

        return texto_email

    except Exception as e:
        print(e)
        return None


def parse_email(email_text):
    # Buscar etiquetas en el texto del correo
    tag_regex = re.compile(r"\*([^\n]+)\n")
    tag_match = tag_regex.search(email_text)
    if tag_match:
        tag = tag_match.group(1)
    else:
        tag = None

    # Buscar nombre en el texto del correo y la cantidad
    name_regex = re.compile(
        r"([A-Za-z]+ [A-Za-z]+) (le ha enviado|le envi=C3=B3) \$(\d+\.\d{2})"
    )
    name_match = name_regex.search(email_text)
    if name_match:
        name = name_match.group(1)
        amount = float(name_match.group(3))
    else:
        name = None
        amount = None

    return (tag, name, amount)


def main():
    # Crear instancia del servicio de Gmail
    gmail_service = construct_service(API_SERVICE_GMAIL)
    if gmail_service is None:
        print("No se pudo crear el servicio de Gmail.")
        return

    print("gmail_service", gmail_service)

    """
    Search emails ()
    """
    # Filtro de búsqueda por el remitente
    query_string = "from:alistdk@gmail.com"

    # Obtener lista de mensajes que cumplen con el filtro de búsqueda
    email_resultados = search_email(gmail_service, query_string, ["INBOX"])

    for mensaje in email_resultados:
        mensaje_id = mensaje["id"]
        mensaje_detalle = get_message_detail(gmail_service, mensaje_id)
        tag1, name1, amount1 = parse_email(mensaje_detalle)
        print("Etiqueta cliente recibe el pago -->", tag1)
        print("Nombre de quien envía -->", name1)
        print("Cantidad del pago -->", amount1)
        print("############-------------------############# ")


if __name__ == "__main__":
    main()