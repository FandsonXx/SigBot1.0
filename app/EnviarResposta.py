import requests
from key import API_URL,TELEGRAM_TOKEN

def enviarPdf(file_path,idchat):
    f = open(file_path, 'rb')
    file_bytes = f.read()
    f.close()
    response = {
        'document': (f.name, file_bytes)
    }
    method_name = 'sendDocument'
    send_response(method_name, response,idchat)


def send_response( method_name, params,idchat):
    if method_name == 'sendDocument':
        document = params['document']
        del params['document']
        r = requests.post(url=API_URL.format(method_name=method_name, chat_id=idchat), params=params,
                          files={'document': document})


    else:
        r = requests.post(url=API_URL.format(method_name=method_name), params=params)
    return r.status_code == 200


def enviarImagem( file_path, idchat):
    body = {
        'chat_id': idchat,
    }
    files = {
        'photo': open(file_path, 'rb')
    }
    r = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(
        TELEGRAM_TOKEN), data=body, files=files)
    print(r)
    if r.status_code >= 400:
        print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))


def responder(resposta, chat_id):
        link_de_envio = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={chat_id}&text={resposta}'

        requests.get(link_de_envio)