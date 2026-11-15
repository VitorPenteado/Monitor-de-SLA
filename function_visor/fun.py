import pandas as pd

CAMINHO = (r"C:\Users\vitor\Downloads\BANCO - SUDESTE-2026-11-14-11-37-29.csv")
df = pd.read_csv(CAMINHO, sep=";", encoding="latin-1")
df["Início agendado"] = pd.to_datetime(df["Início agendado"], dayfirst=True)

def filtrar_conveniencia(dados):
    hoje = pd.Timestamp.now().date()
    
    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Pinned"].astype(str) == "1") &
        (dados["Início agendado"].dt.date > hoje) &
        (~dados["Modificado pela última vez por"].isin(["Datacake", "BOT - Alteracao Pedido Cliente - Alteração por Automacao", "Data.com Clean", "Flow Integration", "Dupla conveniencia"])) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

def filtrar_fixado_bot(dados):
    hoje = pd.Timestamp.now().date()

    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Pinned"].astype(str) == "1") &
        (dados["Início agendado"].dt.date > hoje) &
        (dados["Modificado pela última vez por"].isin(["Datacake", "BOT - Alteracao Pedido Cliente - Alteração por Automacao", "Data.com Clean", "Flow Integration", "Dupla conveniencia"])) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

df_conveniencia = filtrar_conveniencia(df)
print(df_conveniencia[["Número de compromisso", "Início agendado"]])