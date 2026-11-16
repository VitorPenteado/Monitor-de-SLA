# 📊 Monitor de SLA

Ferramenta para leitura e classificação de **Service Appointments (SA)** exportados do Salesforce, indicando a situação de cada OS em relação aos prazos de atendimento.

## 📑 Sumário

- [Visão geral](#-visão-geral)
- [Campos utilizados](#-campos-utilizados)
- [Classificações](#-classificações)
- [Regras de negócio](#-regras-de-negócio)
- [Considerações finais](#-considerações-finais)
- [Interface](#-interface)
- [Back-end](#-back-end)
- [Dados](#-dados)

---

## 🎯 Visão geral

O programa lê uma planilha de dados do Salesforce, organizada em seções de colunas, e valida cada **SA** (código usado para cada OS, ou Ordem de Serviço) com base nas datas de criação, primeiro agendamento, início agendado e conclusão.

Ao final, cada OS é classificada em uma ou mais categorias (veja abaixo).

## 🗂️ Campos utilizados

| Campo | Descrição |
|---|---|
| **SA** | Código da OS |
| **Data de criação** | Quando a OS foi aberta |
| **Data do primeiro agendamento** | Prazo base da OS |
| **Início agendado** | Data/hora agendada para o atendimento |
| **Vencimento VREP** | Prazo adicional (somente Reparos) |
| **Pinned** | Indica se a OS está fixada (`1` = fixada) |
| **Modificado pela última vez** | Último usuário/sistema que alterou a OS |
| **Status** | Situação atual da OS |

> **D0** = data de hoje.

## 🏷️ Classificações

| Classificação | Resumo |
|---|---|
| **Conveniência** | Agendada para o futuro, fixada, e alterada por uma pessoa (não por automação) |
| **Fixado Bot** | Última modificação feita por Bot, Matrix ou Data Clear |
| **Futura** | Data futura e sem fixação |
| **Vencida** | Prazo já expirado |
| **Prazo a vencer** | Prazo ainda dentro da validade |
| **AGE** | OS aberta há mais de 6 dias |
| **Data D0** | Início agendado para hoje |
| **Confirmado D0** | Início agendado para hoje **e** fixada |
| **Em espera** | Sem status ou sem agendamento |

## 📐 Regras de negócio

### Conveniência

```text
SE "Início Agendado" > D0
E  "Pinned" = 1
E  "Modificado pela última vez" NÃO ESTÁ EM [Bot, Matrix, Data Clear]
→ CONVENIÊNCIA
```

### Fixado Bot

```text
SE "Modificado pela última vez" ESTÁ EM [Bot, Matrix, Data Clear]
→ FIXADO BOT
→ exibir: "Validar Serviços fixados Bot"
```

### Futura

OS em data futura **sem** estar fixada (`Pinned != 1`). Dentro dela, aplica-se a regra de prazo:

#### Vencida

```text
SE "Data do primeiro agendamento" < D0
OU "Vencimento VREP" < D0
→ VENCIDA
SENÃO → PRAZO A VENCER
```

#### Prazo a vencer

```text
SE "Data do primeiro agendamento" >= D0
E  "Vencimento VREP" >= D0
→ PRAZO A VENCER
SENÃO → VENCIDA
```

### AGE

```text
SE "Data de criação" + 6 dias < D0   (OS aberta há mais de 6 dias)
→ AGE = Verdadeiro
SENÃO → AGE = Falso
```

> ℹ️ Uma OS **AGE** pode pertencer a qualquer uma das classificações anteriores.

### Data D0

```text
SE "Início Agendado" = D0
→ DATA D0
SENÃO → FUTURA
```

### Confirmado D0

```text
SE "Início Agendado" = D0
E  "Pinned" = 1
→ CONFIRMADO D0
SENÃO → DATA D0
```

### Em espera

```text
SE "Status" = "Nenhuma"
→ EM ESPERA
```

## ✅ Considerações finais

- Todas as OS possuem prazo pela **"Data do primeiro agendamento"**. Somente os **Reparos** somam a ela o **"Vencimento VREP"**.
- Uma OS é **Vencida** ou **Prazo a vencer**: não existe terceira possibilidade.
- OS sem **"Início Agendado"** ou sem **"Data do primeiro agendamento"** são tratadas como agendamentos em **Espera**.

## 🖥️ Interface

> 🚧 *Em construção.*

## ⚙️ Back-end

Script em **Python** com **pandas**. O fluxo é:

1. Lê o CSV exportado do sistema.
2. Converte as colunas de data.
3. Aplica um filtro por classificação.
4. Gera um DataFrame para cada classificação.

### Dependências

```bash
pip install pandas
```

### Fluxo de processamento

| Etapa | Descrição |
|---|---|
| **Leitura** | `pd.read_csv` com separador `;` e encoding `latin-1` |
| **Datas** | `Início agendado` é convertido com `dayfirst=True`. `Limite_CA` é criado a partir de `Data do Primeiro Agendamento` (data + hora final do texto) |
| **Filtros** | Uma função por classificação, todas restritas à regional **TERRITÓRIO JUNDIAÍ** |
| **Saída** | Um DataFrame por classificação |

### Funções de classificação

| Função | Classificação | Critérios |
|---|---|---|
| `filtrar_conveniencia` | Conveniência | `Pinned = 1`, início agendado após hoje, modificado por usuário **que não é bot**, status ≠ `Nenhuma` |
| `filtrar_fixado_bot` | Fixado Bot | Mesmos critérios, mas modificado por usuário **da lista de bots** |
| `is_ca_vencido` | CA vencido | `Limite_CA` é hoje e já passou do horário atual, tipo de trabalho na lista, status ≠ `Nenhuma` |
| `is_ca_prazo` | CA no prazo | `Limite_CA` é hoje ou depois e ainda não passou do horário atual, tipo de trabalho na lista, status ≠ `Nenhuma` |
| `entrante` | Entrante | Início agendado após hoje, `Pinned = 0`, tipo de trabalho na lista, status ≠ `Nenhuma` |

### Listas de apoio

**Usuários considerados bot**

- `Datacake`
- `BOT - Alteracao Pedido Cliente - Alteração por Automacao`
- `Data.com Clean`
- `Flow Integration`
- `Dupla conveniencia`

**Tipos de trabalho considerados**

- Mudança de endereço
- Manutenção
- Ativação

## 🗃️ Dados

### Fonte

CSV exportado do sistema, no formato `BANCO - SUDESTE-AAAA-MM-DD-HH-MM-SS.csv`, salvo na pasta de Downloads. O caminho é definido na constante `CAMINHO`.

### Colunas utilizadas

| Coluna | Uso |
|---|---|
| `Regional` | Filtro fixo: `TERRITÓRIO JUNDIAÍ` |
| `Pinned` | Fixação da OS (`1` = fixada, `0` = não fixada) |
| `Início agendado` | Comparação com a data de hoje |
| `Data do Primeiro Agendamento` | Origem do `Limite_CA` |
| `Modificado pela última vez por` | Identifica se a alteração foi de bot ou de pessoa |
| `Status da Ordem de Serviço` | OS com status `Nenhuma` são excluídas |
| `Tipo de Trabalho` | Filtro nas classificações de CA e Entrante |

### Colunas calculadas

| Coluna | Descrição |
|---|---|
| `Limite_CA` | Data e hora limite do CA, extraídas de `Data do Primeiro Agendamento` (formato `dd/mm/aaaa hh:mm`). Valores inválidos viram `NaT` |