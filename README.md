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

> 🚧 *Em construção.*

## 🗃️ Dados

> 🚧 *Em construção.*