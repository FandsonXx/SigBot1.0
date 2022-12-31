import os
from pathlib import Path

caminho_salvapdf = Path(__file__)
caminho = caminho_salvapdf.parent

def remover(): #funçao para esvaziar a pasta de arquivos temporario (historicos e notas geradas pelo app)
    dir = '{}'.format(caminho.parent / "files")
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))



