import pandas as pd

CAMINHO = (r"C:\Users\vitor\Downloads\BANCO - SUDESTE-2026-11-14-11-37-29.csv")
df = pd.read_csv(CAMINHO, sep=";", encoding="latin-1")
df["Início agendado"] = pd.to_datetime(df["Início agendado"], dayfirst=True)

usuarios_bot = [
        "Datacake",
        "BOT - Alteracao Pedido Cliente - Alteração por Automacao",
        "Data.com Clean",
        "Flow Integration",
        "Dupla conveniencia"
    ]

tipo_trabalho = [
    "Mudança de endereço",
    "Manutenção",
    "Ativação"
]

def filtrar_conveniencia(dados):
    hoje = pd.Timestamp.now().date()
    
    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Pinned"].astype(str) == "1") &
        (dados["Início agendado"].dt.date > hoje) &
        (~dados["Modificado pela última vez por"].isin(usuarios_bot)) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

def filtrar_fixado_bot(dados):
    hoje = pd.Timestamp.now().date()


    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Pinned"].astype(str) == "1") &
        (dados["Início agendado"].dt.date > hoje) &
        (dados["Modificado pela última vez por"].isin(usuarios_bot)) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

data_texto = df["Data do Primeiro Agendamento"].astype(str).str[:10]
hora_final_texto = df["Data do Primeiro Agendamento"].astype(str).str.strip().str[-5:]
df["Limite_CA"] = pd.to_datetime(
    data_texto + " " + hora_final_texto, 
    format="%d/%m/%Y %H:%M", 
    errors="coerce"
)

def is_ca_vencido(dados):
    hoje = pd.Timestamp.now().date()
    agora = pd.Timestamp.now()

    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Limite_CA"].dt.date >= hoje) &
        (dados["Limite_CA"] <= agora) &
        (dados["Tipo de Trabalho"].isin(tipo_trabalho)) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

def is_ca_prazo(dados):
    hoje = pd.Timestamp.now().date()
    agora = pd.Timestamp.now()

    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Limite_CA"].dt.date >= hoje) &
        (dados["Limite_CA"] > agora) &
        (dados["Tipo de Trabalho"].isin(tipo_trabalho)) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

def entrante(dados):
    hoje = pd.Timestamp.now().date()
    agora = pd.Timestamp.now()

    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Início agendado"].dt.date > hoje) &
        (dados["Pinned"].astype(str) == "0") &
        (dados["Tipo de Trabalho"].isin(tipo_trabalho)) &
        (dados["Status da Ordem de Serviço"] != "Nenhuma")
    )
    return dados.loc[filtro]

def em_espera(dados):
    hoje = pd.Timestamp.now().date()
    agora = pd.Timestamp.now()

    filtro = (
        (dados["Regional"] == "TERRITÓRIO JUNDIAÍ") &
        (dados["Status da Ordem de Serviço"] == "Nenhuma")
    )
    return dados.loc[filtro]

df_conveniencia = filtrar_conveniencia(df)
df_fixado_bot = filtrar_fixado_bot(df)
df_vencidos = is_ca_vencido(df)
df_prazo = is_ca_prazo(df)
df_entrante = entrante(df)
df_espera = em_espera(df)
print(df_espera[["Número de compromisso", "Início agendado", "Data do Primeiro Agendamento"]])