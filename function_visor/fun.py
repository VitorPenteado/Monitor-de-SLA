import pandas as pd

CAMINHO = (r"C:\Users\vitor\Downloads\BANCO - SUDESTE-2026-11-14-11-37-29.csv")

df = pd.read_csv(CAMINHO, sep=";", encoding="latin-1")

def conveniencia(SA):
    df.loc[df["Regional"]=="TERRITÓRIO JUNDIAÍ","Compromisso de Serviço"]
    return "Compromisso de Serviço"