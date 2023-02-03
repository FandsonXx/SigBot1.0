from selenium import webdriver
import Avisos
from pathlib import Path

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent

"""
Este código é uma função em Python que realiza o login em um sistema acadêmico chamado SigUEma. 
A função utiliza o selenium webdriver para abrir uma instância do Chrome em modo headless, 
navegar até a página de login, preencher os campos de usuário e senha e clicar no botão de 
login. Em seguida, o código verifica se houve algum erro de login ou se o login foi bem-sucedido. 
Se houve erro, ele procura um elemento na página que indica o erro e retorna um objeto com uma 
mensagem de aviso. Se não houve erro, ele retorna outro objeto sem aviso.
"""

class Sessao:
    def loginsistema(user, senha, pedido):  # funçao que faz o login  no sistema academico SigUEma
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": r"{}".format(caminho.parent / "files"),
                 # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        chromeOptions.add_argument("--headless")
        chromeOptions.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(options=chromeOptions)
        browser.get('https://sis.sig.uema.br/sigaa/verTelaLogin.do')
        username = browser.find_element("name", "user.login")
        password = browser.find_element("name", "user.senha")
        username.send_keys(user)
        password.send_keys(senha)
        browser.find_element("xpath", '/html/body/div[2]/div[2]/div[3]/form/table/tfoot/tr/td/input').click()
        try:
            element = browser.find_element("xpath", "/html/body/div[2]/div[2]/center[2]")
            browser.close()
            return 1

        except:
            try:
                element = browser.find_element("name", "j_id_jsp_1443629000_1:j_id_jsp_1443629000_2")
                txt = element.is_displayed()
                return Avisos.Aviso(txt, browser, pedido)
            # element = browser.find_element("name", "j_id_jsp_1443629000_1:j_id_jsp_1443629000_2")
            except:
                return Avisos.Semaviso(pedido, browser)


darss = Sessao

darss.loginsistema("05195989389", "Wather1234", 1)
