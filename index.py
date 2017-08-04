import os
from flask import Flask, request
import requests
import traceback
import json
import urllib.request


token = ('EAAD7dPJ5iFQBAIVfiDAh1h4zMd4CxcCSVASniXCvAsE6cDJyI8D2HzgPeAz6ZAhSvFgh4ZACKTVKvKdtJWOGOntWngdW1TITiNzHpc7xTY6HfdRiwt05JKfi46iXqi65yg8RlBxgU6K5RBiUJrfTZA8SB5qMGgQUjyGZBL3EHQZDZD')
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            text = data['entry'][0]['messaging'][0]['message']['text']
            sender = data['entry'][0]['messaging'][0]['sender']['id']
            
            url = 'https://api.thingspeak.com/channels/311371/feeds.json?api_key=GFFW6MZQNLW7L5UP&results=1'
            r = urllib.request.urlopen(url)
            resposta = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
            
            temp = resposta['feeds'][0]['field1']
            pre = resposta['feeds'][0]['field2']
            alt = resposta['feeds'][0]['field3']
            chuva = resposta['feeds'][0]['field4']

            if "temperatura" in text:
                resposta = "A temperatura é de " + temp +"°C"
            elif "pressão" in text:
                resposta = "A pressão atmosferica é "+pre+" atm"
            elif "altitude" in text:
                resposta = "A altitude é "+alt+" metros"
            elif "chover" in text:
                if (chuva == "0"):
                    resposta = "Sim esta a chover!!!"
                else:
                    resposta = "Não esta a chover!!!"
            else:
                resposta = "Não tenho capacidade para responder a isso!!"


            payload = {'recipient': {'id': sender}, 'message': {'text': resposta}}
            r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
        except Exception as e:
            print(traceback.format_exc())


    elif request.method == 'GET': # Para a verificação inicial
        if request.args.get('hub.verify_token') == ('olamundojlkjdlxfjklxjclfxdclxkclxjkl'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"

if __name__ == '__main__':
    app.run(debug=True)