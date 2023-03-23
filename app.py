from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# Configurar los tokens y claves necesarios
VERIFY_TOKEN = os.environ.get('secret')
PAGE_ACCESS_TOKEN = os.environ.get('EAAIjI4ZBs4BIBAOjb55btaqXmGVhqQXl06W1WNDfOamm2NnVZAuCx1IIDBzBFSVIWdZByZAu8ZCjqbZBeD0qpCE9WOSqqYkSaEJVvlh8PHpNAvwNxt2PbUT9ZAMZAWzzhe64klJt7VGmcgfsFnpkw8q9Nck5P90UVH1T6ylgZAJZC4sPHCDjgDQogkNKeSZBiEkI1kZD')

# Endpoint para el webhook de Facebook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificar el token de verificación
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        else:
            return 'Invalid verification token'
    elif request.method == 'POST':
        # Procesar la notificación de Facebook
        data = request.get_json()
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # Verificar si el mensaje es de un usuario y no del bot
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']
                    message_text = messaging_event['message']['text']
                    # Realizar una acción específica en función del mensaje recibido
                    # Por ejemplo, enviar una respuesta personalizada
                    send_message(sender_id, 'Gracias por tu mensaje: ' + message_text)
        return 'OK'

# Función para enviar un mensaje a un usuario de Facebook
def send_message(recipient_id, message_text):
    params = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': message_text
        }
    }
    response = requests.post('https://graph.facebook.com/v12.0/me/messages', params=params, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print('Error al enviar el mensaje: ' + response.text)
