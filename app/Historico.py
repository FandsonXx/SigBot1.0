import time

def getHistorico(browser):
    idmatricula = browser.find_element("xpath",
                                       "/html/body/div[2]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[1]/td[2]").text

    element = browser.find_element("xpath",
                                   "/html/body/div[2]/div[2]/div[1]/div[1]/div/form/div/table/tbody/tr/td[1]/span[2]").click()
    element = browser.find_element("xpath",
                                   "/html/body/div[2]/div[2]/div[1]/div[1]/div/form/div/div[1]/table/tbody/tr[4]/td[2]").click()
    time.sleep(20)
    return idmatricula