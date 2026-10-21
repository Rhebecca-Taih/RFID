<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Impress%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Impressão"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    A pessoa escolhe Data, Setor, Etiqueta e Impressora; o robô lê os<br>
    pedidos aprovados, configura cada um no portal web e imprime —<br>
    avaliando por critério próprio quando a impressão não é necessária.
  </samp>
</div>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=deaaf9" alt="Python" />
  <img src="https://img.shields.io/badge/Selenium-000000?style=for-the-badge&logo=selenium&logoColor=deaaf9" alt="Selenium" />
  <img src="https://img.shields.io/badge/status-finalizado-8323B5?style=for-the-badge" alt="Status: finalizado" />
</div>

<br>

## ⋆˚✮ Contexto

Terceira etapa do pipeline de aprovação de pedidos: a partir do que o
Aprovador já aprovou, configura etiqueta e impressora e imprime cada
pedido diretamente no portal web, analisando por critério próprio a
necessidade de impressão em diferentes modos.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Impressão configurada | Define etiqueta e impressora no portal antes de imprimir cada pedido |
| Análise por critério | Avalia, para cada pedido já processado por fora, se a impressão é realmente necessária |
| Consulta a planilha auxiliar | Confere disponibilidade de etiqueta física já impressa numa fonte auxiliar, por setor |
| Histórico versionado | Cria um histórico de impressão com status de cada pedido, por data e setor |
| Seletores configuráveis | Todos os seletores do portal ficam num arquivo JSON separado |

## ⋆˚✮ Destaques técnicos

- **Cliques atômicos via JavaScript** — localizar o elemento, rolar até a
  área visível e clicar acontecem num único comando, executado pelo
  próprio navegador.
- **Cópia local somente leitura da base mestra** — nunca abre o arquivo de
  rede diretamente; outro robô pode estar escrevendo nele ao mesmo tempo.
- **Lock distribuído com heartbeat** — impede que duas máquinas processem
  o mesmo lote ao mesmo tempo; se a máquina ativa parar de responder por
  mais de duas horas, outra assume o processamento automaticamente.
- **Seletores em arquivo JSON separado** — quando o portal muda, o ajuste
  é só ali, sem tocar em código.
- **Auto-instalação** — dependências e cópia do Chrome/Driver da rede na
  primeira execução em cada máquina, em etapas visíveis na tela antes da
  escolha de Data e Setor.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Pessoa escolhe Data + Setor + Etiqueta + Impressora e clica em Processar
│
├─ Junta todos os ciclos de aprovação daquele dia/setor
│
├─ Processa cada pedido
│   ├─ Aprovado                → configura Etiqueta + Impressora,
│   │                             salva, confere e imprime
│   └─ Já processado por fora  → classificado pelo critério de
│                                 necessidade de impressão
│
└─ Grava um histórico de impressão, com status de cada pedido
```

O acesso ao portal usa as credenciais da configuração compartilhada
(`Config_Cg/.env`). Cada clique acontece num único
comando JavaScript atômico, a partir do XPath configurado no JSON de
seletores.

### ✮ Pré-Requisitos

Este robô depende da rede corporativa e do portal de pedidos — não é
executável fora desse ambiente, nem para teste. Este repositório está
publicado como peça de portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Interpretador que executa o robô |
| Windows | Único sistema operacional suportado |
| Acesso à rede corporativa | Cópia do Chrome/Driver, portal de pedidos e base mestra de pedidos |

### ✮ Configuração

⋆˚✮ A configuração real fica em `../Config_Cg/.env` (não versionado).
Referências em `../Config_Cg/env.exemplo`.

| Variável | O que controla |
| :--- | :--- |
| `CAMINHO_REDE_BASE_GERAL` | Cópia de rede da base mestra de pedidos, lida como referência |
| `LINK_COLMEIA_ARTIGOS` | Link público de planilha auxiliar com etiquetas físicas disponíveis |
| `MODELOS_ETIQUETA_IMPRESSAO` / `IMPRESSORAS_DISPONIVEIS` | Opções disponíveis na tela (opcional, já tem um padrão) |

Credenciais e URL do portal vêm da mesma seção do `.env` usada pelo
Aprovador.

## ⋆˚✮ Stack

`Python 3.10+` · `Selenium` · `customtkinter` · `pystray` · `openpyxl` ·
Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
