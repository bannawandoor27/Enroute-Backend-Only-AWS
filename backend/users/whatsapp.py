from whatsapp_api_client_python import API
from django.conf import settings


greenAPI = API.GreenApi(settings.WHATSAPP_ID,settings.WHATSAPP_TOKEN)

def send_whatsapp_message(message,number):
    result=greenAPI.sending.sendMessage(f'91{number}@c.us', message)
    print(result.data)