
import tabelaNotas
import Historico


def Aviso(txt, browser,pedido):
        try:
            while txt:
                element = browser.find_element("name", "j_id_jsp_1443629000_1:j_id_jsp_1443629000_2").click()
        finally:
          return  Semaviso(pedido,browser)


def Semaviso(pedido,browser):
        if pedido == 1:
            return tabelaNotas.getNotas(browser)
        if pedido == 2:
            return Historico.getHistorico(browser)