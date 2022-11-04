# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_notif_whats(phone, body):
    account_sid = 'AC20bb5fc8ca8d48d9eea294e00f15c3ce' 
    auth_token = 'ccab37bd91efc69d1f70e85e3ab40602' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create( 
                                from_='+18316180989',  
                                body=body,
                                to=phone 
                            ) 
    
    print('Envoyè avec success')
