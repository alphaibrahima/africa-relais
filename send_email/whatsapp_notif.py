# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from delivery_management.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.http import HttpResponse
from django.shortcuts import render

import http.client
import json



# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_notif_whats(phone, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)    
    message = client.messages.create( 
                                from_='whatsapp:+19377499719',  
                                body=body,
                                to=phone 
                            ) 
    
    print('Envoyè avec success')



def send_notif_infobip(phone, body):
    conn = http.client.HTTPSConnection("5vnnlg.api.infobip.com")
    payload = json.dumps({
        "from": "441134960000",
        "to": "221772733355",
        "messageId": "a28dd97c-1ffb-4fcf-99f1-0b557ed381da",
        "content": {
            "text": "Some text"
        },
        "callbackData": "Callback data",
        "notifyUrl": "https://www.example.com/whatsapp"
    })
    headers = {
        'Authorization': '{authorization}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/whatsapp/1/message/text", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
