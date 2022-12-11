import requests
import json5
import IniciarSessao
from pathlib import Path
import RemoverArquivos

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent

TELEGRAM_TOKEN = '5639397237:AAHOaMa2mEJ79X76NbxxWol-9NqrT_4E0vs'
API_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}' + '/{method_name}' + '?chat_id={chat_id}'


# ler as mensagens
class TelegramBot:
    def __init__(self):
        self.login = None
        self.token = '5639397237:AAHOaMa2mEJ79X76NbxxWol-9NqrT_4E0vs'
        self.url_base = f'https://api.telegram.org/bot{self.token}'
        self.senha = None
        self.identificador = None
        self.idchat = None

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)

            mensagens = atualizacao['result']
            if mensagens:
                for mensagem in mensagens:
                    update_id = mensagem['update_id']
                    chat_id = mensagem['message']['from']['id']
                    self.idchat = chat_id
                    primeiramensagem = mensagem['message']['from']['id']
                    resposta = self.criar_resposta(mensagem, primeiramensagem)
                    self.responder(resposta, chat_id)

    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}/getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json5.loads(resultado.content)

    def criar_resposta(self, mensagem, primeiramensagem, ):
        mensagem = mensagem['message']['text']
        if primeiramensagem == True or mensagem.lower() in ('/menu', 'menu'):
            RemoverArquivos.remover()
            return f"""Ola Bem vindo ao sigBot.digite a opçao desejada abaixo 
                       1. Notas/Faltas 
                       2. Historico"""
        if mensagem == '1' or mensagem.lower() in ('/notas', 'notas') or self.identificador == 3:
            self.identificador = 1
            return f'''Otimo! agora digite seu login 
                        *Seus dados nao serão salvos no sistema*'''
        if mensagem.lower() in ('histórico', '/histórico', '/historico', 'historico', '2') or self.identificador == 4:
            self.identificador = 2
            return f'''Otimo! agora digite seu login
                       *Seus dados nao serão salvos no sistema*
                        '''
        if len(mensagem) == 11:
            self.login = mensagem
            self.senha = 1
            return f'''agora digite sua senha 
                      Se identificou algum erro digite o login novamente'''
        if  self.senha == 1:
            self.senha = mensagem
            return f'''Digite ok para continuar '''

        if self.identificador == 1 and self.senha != None:
            self.enviar_imagem(caminho.parent / "img" / "wait.gif")
            ass = IniciarSessao.Sessao.login(self.login, self.senha, 1)
            self.identificador = self.validarLogin(ass)
            if self.identificador == 3:
                return 'Ops Senha invalida digite "ok" para tentar novamente '
            self.enviar_imagem(caminho.parent / "files" / "notas.png")
            self.login = None
            self.senha = None
            self.identificador =None
            return f'''para retornar digite menu '''
        if self.identificador == 2 and self.senha != None:
            self.enviar_imagem(caminho.parent / "img" / "wait.gif")
            ass = IniciarSessao.Sessao.login(self.login, self.senha, 2)
            self.identificador = self.validarLogin(ass)
            if self.identificador == 4:
                return 'Ops Senha invalida digite "ok" para tentar novamente '
            pdf = caminho.parent / "files" / "./historico_{}.pdf".format(ass)
            self._send_local_file(pdf)
            self.login = None
            self.senha = None
            self.identificador = None
            return f'''para retornar digite menu '''
        else:
            return 'açao invalida digite o numero correto ou /menu'

    def responder(self, resposta, chat_id):
        link_de_envio = f'{self.url_base}/sendMessage?chat_id={chat_id}&text={resposta}'

        requests.get(link_de_envio)

    def _send_local_file(self, file_path):
        f = open(file_path, 'rb')
        file_bytes = f.read()
        f.close()
        response = {
            'document': (f.name, file_bytes)
        }
        method_name = 'sendDocument'
        self.send_response(method_name, response)

    def send_response(self, method_name, params):
        if method_name == 'sendDocument':
            document = params['document']
            del params['document']
            r = requests.post(url=API_URL.format(method_name=method_name, chat_id=self.idchat), params=params,
                              files={'document': document})


        else:
            r = requests.post(url=API_URL.format(method_name=method_name), params=params)
        return r.status_code == 200

    def enviar_imagem(self, file_path):
        body = {
            'chat_id': self.idchat,
        }
        files = {
            'photo': open(file_path, 'rb')
        }
        r = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(
            self.token), data=body, files=files)
        print(r)
        if r.status_code >= 400:
            print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))


    def validarLogin(self,ass):
        if ass == 1:
            if self.identificador == 1:
                return 3
            if self.identificador == 2:
                return 4
        else:
            return ass


