
from selenium import webdriver
import Avisos
from pathlib import Path

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent

class Sessao:
    def login(user, senha, pedido):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": r"{}".format(caminho.parent / "files"), # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        chromeOptions.add_argument("--headless")
        chromeOptions.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome( chrome_options=chromeOptions)
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


#Sessao.login('05195989389','Wather1234',2)