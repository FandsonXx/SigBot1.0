
from obterMensagemBot import obter_mensagens
from criarResposta import criar_resposta
from EnviarResposta import responder



class TelegramBot:

    def Iniciar(self): #inicia o bot
        update_id = None
        while True:
            atualizacao = obter_mensagens(update_id)
            if "result" in atualizacao:
                mensagens = atualizacao['result']
                if mensagens:
                    for mensagem in mensagens:
                        if "message" in mensagem:
                            update_id = mensagem['update_id']
                            chat_id = mensagem['message']['from']['id']
                            primeiramensagem = mensagem['message']['from']['id']
                            resposta = criar_resposta(mensagem, primeiramensagem,chat_id)
                            responder(resposta, chat_id)






