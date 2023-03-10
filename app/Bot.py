import requests
from key import API_URL, TELEGRAM_TOKEN
import json
from pathlib import Path
from IniciarSessao import Sessao
import RemoverArquivos

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent



#Esse código é uma implementação de um bot do Telegram que
#fornece informações sobre notas e histórico escolar aos usuários.
#O bot usa a biblioteca requests para fazer requisições HTTP à API
#do Telegram e obter as mensagens dos usuários. O bot armazena o
#estado de cada conversa (login, senha e opção escolhida pelo usuário)
#em variáveis de instância e o mantém durante toda a conversa.

class TelegramBot:

    def __init__(self):
        self.senha = None
        self.login = None
        self.opcao = None

    def Iniciar(self):  # O método Iniciar é a rotina principal do bot e é responsável por atualizar e obter novas mensagens dos usuários, criar uma resposta adequada e enviá-la de volta ao usuário
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            if "result" in atualizacao:
                mensagens = atualizacao['result']
                if mensagens:
                    for mensagem in mensagens:
                        if "message" in mensagem:
                            update_id = mensagem['update_id']
                            chat_id = mensagem['message']['from']['id']
                            primeiramensagem = mensagem['message']['from']['id']
                            resposta = self.criar_resposta(mensagem, primeiramensagem, chat_id)
                            self.responder(resposta, chat_id)

    def obter_mensagens(self, update_id):  # obter mensagem do bot no telegram
        link_requisicao = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def criar_resposta(self, mensagem, primeiramensagem,
                       idchat):  # mensagem e opçoes que pareceram para o usuario do bot

        mensagem = mensagem['message']['text']

        if primeiramensagem == True or mensagem.lower() in ('/menu', 'menu'):
            return self.primeira_mensagem()
        if mensagem.lower() in ('/notas', 'notas', '1'):
            return self.opcao_notas("")
        if mensagem.lower() in ('histórico', '/histórico', '/historico', 'historico', '2'):
            return self.opcao_historico("")
        if len(mensagem) == 11 or (self.senha is None and self.login is not None):
            return self.login_senha(mensagem)
        if self.opcao == 1 or self.opcao == 2 and self.senha is not None:
            return self.validacao_sistema(idchat, self.opcao, self.login, self.senha)
        else:
            return 'açao invalida digite o numero correto ou /menu'

    def primeir_amensagem(self):
        RemoverArquivos.remover()
        self.limpa_variaveis()
        return f"""Ola Bem vindo ao sigBot.digite a opção desejada abaixo
                    1. Notas/Faltas
                    2. Historico"""

    def opcao_notas(self, loginivalid):
        self.opcao = 1
        return "{}".format(loginivalid) + '''digite seu login
                                *Seus dados nao serão salvos no sistema*'''

    def opcao_historico(self, loginivalid):
        self.opcao = 2
        return "{}".format(loginivalid) + '''digite seu login
                                *Seus dados nao serão salvos no sistema*'''

    def login_senha(self, mensagem):

        if self.login is None or len(mensagem) == 11:
            self.login = mensagem
            return f'''agora digite sua senha
                             Se identificou algum erro digite o login novamente'''
        if self.login is not None:
            self.senha = mensagem
            return f'''Digite ok para continuar'''

    def validacao_sistema(self, idchat, opc, login, senha):
        self.enviarImagem(caminho.parent / "img" / "wait.gif", idchat)
        nmatricula = Sessao.loginsistema(login, senha, opc)
        if nmatricula == 1:
            return self.login_incorreto(opc)
        return self.preparacao_documento(opc, idchat, nmatricula)

    def preparacao_documento(self, opc, idchat, nmatricula):
        if opc == 1:
            self.enviarImagem(caminho.parent / "files" / "notas.png", idchat)
        if opc == 2:
            self.enviarPdf(nmatricula, idchat)
        return f'''para retornar digite menu '''

    def login_incorreto(self, identificador):  # funçao para identificar se o login no sistema foi feito
        loginivalid = '''Ops Senha invalida que tentar novamente? 
                      '''
        if identificador == 1:
            return self.opcao_notas(loginivalid)
        if identificador == 2:
            return self.opcao_historico(loginivalid)

    def limpa_variaveis(self):
        self.login = None
        self.senha = None
        self.opcao = None

    def enviarPdf(self, aux, idchat):  # funçao para enviar o arquivo pdf
        pdf = caminho.parent / "files" / "./historico_{}.pdf".format(aux)
        f = open(pdf, 'rb')
        file_bytes = f.read()
        f.close()
        response = {
            'document': (f.name, file_bytes)
        }
        method_name = 'sendDocument'
        self.send_response(method_name, response, idchat)

    def send_response(self, method_name, params, idchat):
        if method_name == 'sendDocument':
            document = params['document']
            del params['document']
            r = requests.post(url=API_URL.format(method_name=method_name, chat_id=idchat), params=params,
                              files={'document': document})
            self.limpa_variaveis()
        else:
            r = requests.post(url=API_URL.format(method_name=method_name), params=params)
            self.limpa_variaveis()
        return r.status_code == 200

    def enviarImagem(self, file_path, idchat):  # para enviar imagens

        body = {
            'chat_id': idchat,
        }
        files = {
            'photo': open(file_path, 'rb')
        }
        r = requests.post('https://api.telegram.org/bot{}/sendPhoto'.format(
            TELEGRAM_TOKEN), data=body, files=files)
        self.limpa_variaveis()
        print(r)
        if r.status_code >= 400:
            print('Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text))

    def responder(self, resposta, chat_id):
        link_de_envio = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={chat_id}&text={resposta}'

        requests.get(link_de_envio)
