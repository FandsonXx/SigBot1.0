from pathlib import Path
import EnviarResposta
import IniciarSessao
import RemoverArquivos
import key

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent

def criar_resposta(mensagem, primeiramensagem, idchat):

    mensagem = mensagem['message']['text']

    if primeiramensagem == True or mensagem.lower() in ('/menu', 'menu'):
        RemoverArquivos.remover()
        return f"""Ola Bem vindo ao sigBot.digite a opçao desejada abaixo
                   1. Notas/Faltas
                   2. Historico"""
    if mensagem == '1' or mensagem.lower() in ('/notas', 'notas') or key.identificador == 3:
        key.identificador = 1
        return f'''Otimo! agora digite seu login
                    *Seus dados nao serão salvos no sistema*'''
    if mensagem.lower() in ('histórico', '/histórico', '/historico', 'historico', '2') or key.identificador == 4:
        key.identificador = 2
        return f'''Otimo! agora digite seu login
                   *Seus dados nao serão salvos no sistema*
                    '''
    if len(mensagem) == 11:
        key.login = mensagem
        key.senha = 1
        return f'''agora digite sua senha
                  Se identificou algum erro digite o login novamente'''
    if  key.senha == 1:
        key.senha = mensagem
        return f'''Digite ok para continuar '''

    if key.identificador == 1 and key.senha != None:
        EnviarResposta.enviarImagem(caminho.parent / "img" / "wait.gif",idchat)
        ass = IniciarSessao.Sessao.login(key.login, key.senha, 1)
        key.identificador = validarLogin(ass,key.identificador)
        if key.identificador == 3:
            return 'Ops Senha invalida digite "ok" para tentar novamente '
        EnviarResposta.enviarImagem(caminho.parent / "files" / "notas.png",idchat)
        key.login = None
        key.senha = None
        key.identificador =None
        return f'''para retornar digite menu '''
    if key.identificador == 2 and key.senha != None:
        EnviarResposta.enviarImagem(caminho.parent / "img" / "wait.gif",idchat)
        ass = IniciarSessao.Sessao.login(key.login, key.senha, 2)
        key.identificador = validarLogin(ass,key.identificador)
        if key.identificador == 4:
            return 'Ops Senha invalida digite "ok" para tentar novamente '
        pdf = caminho.parent / "files" / "./historico_{}.pdf".format(ass)
        EnviarResposta.enviarPdf(pdf,idchat)
        key.login = None
        key.senha = None
        key.identificador = None
        return f'''para retornar digite menu '''
    else:
        return 'açao invalida digite o numero correto ou /menu'


def validarLogin(ass,identificador):
        if ass == 1:
            if identificador == 1:
                return 3
            if identificador == 2:
                return 4
        else:
            return ass