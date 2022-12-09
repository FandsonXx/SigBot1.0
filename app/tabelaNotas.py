import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import dataframe_image as dfi
from pathlib import Path

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent

def getNotas(browser):
    browser.find_element("xpath",
                                   "/html/body/div[2]/div[2]/div[1]/div[1]/div/form/div/table/tbody/tr/td[1]/span[2]").click()
    browser.find_element("xpath",
                                   "/html/body/div[2]/div[2]/div[1]/div[1]/div/form/div/div[1]/table/tbody/tr[1]/td[2]").click()
    table = browser.find_element("xpath", "/html/body/div[1]/div[2]/div/table[1]")
    htmlContent = table.get_attribute("outerHTML")
    soup = BeautifulSoup(htmlContent, 'html.parser')

    dados = pd.read_html(htmlContent, encoding='utf-8', decimal=",", thousands='.', converters={'Account': str})

    df = dados[0].copy()
    df.drop(["Media", "Faltas", "Código", "Situação"], axis=1, inplace=True)
    df2 = df.replace(np.nan, '', regex=True)
    dfi.export(df2, "{}".format(caminho.parent / "files" / "notas.png"))
    print(df.to_string())
    browser.close()
    return (df2.to_string())