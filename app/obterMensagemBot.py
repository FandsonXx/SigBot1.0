from key import TELEGRAM_TOKEN
import requests
import json

def obter_mensagens(update_id):
    link_requisicao = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?timeout=100'
    if update_id:
        link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
    resultado = requests.get(link_requisicao)
    return json.loads(resultado.content)