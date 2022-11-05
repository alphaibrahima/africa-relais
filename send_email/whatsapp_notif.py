# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_notif_whats(phone, body):
    account_sid = '' 
    auth_token = '' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create( 
                                from_='+18316180989',  
                                body=body,
                                to=phone 
                            ) 
    
    print('Envoyè avec success')
