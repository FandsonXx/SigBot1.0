
import tabelaNotas
import Historico


def Aviso(txt, browser,pedido): # funçao para passar pelo avisos que aparecem antes da pagina inicial
        try:
            while txt:
                element = browser.find_element("name", "j_id_jsp_1443629000_1:j_id_jsp_1443629000_2").click()
        finally:
          return  Semaviso(pedido,browser)


def Semaviso(pedido,browser): # quando nao tiver aviso antes da pagina inicial
        if pedido == 1:
            return tabelaNotas.getNotas(browser)
        if pedido == 2:
            return Historico.getHistorico(browser)