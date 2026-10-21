<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Rob%C3%B4s%20Bureau%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Robôs Bureau"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    Três robôs em sequência automatizam a etapa de aprovação e<br>
    impressão de pedidos: preparar a query, aprovar no portal web<br>
    e imprimir o que foi aprovado.
  </samp>
</div>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=deaaf9" alt="Python" />
  <img src="https://img.shields.io/badge/Selenium-000000?style=for-the-badge&logo=selenium&logoColor=deaaf9" alt="Selenium" />
  <img src="https://img.shields.io/badge/Excel_·_win32com-000000?style=for-the-badge&logo=microsoftexcel&logoColor=deaaf9" alt="Excel / win32com" />
  <img src="https://img.shields.io/badge/status-finalizado-8323B5?style=for-the-badge" alt="Status: finalizado" />
</div>

<br>

## ⋆˚✮ Contexto

Três robôs cuidam, em sequência, da etapa de aprovação e impressão de
pedidos de etiqueta RFID: o [Preparador](./Preparador) prepara a fila, o
[Aprovador](./Aprovador) confere e aprova no portal, e a
[Impressão](./Impressão) configura e imprime o que foi aprovado. Cada um
entrega o trabalho ao próximo por meio de arquivos.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Preparação de fila | Atualiza a consulta de pedidos a partir da data e do setor escolhidos |
| Aprovação automática | Confere artigo, quantidade e modelo de cada pedido e aprova os que estão de acordo |
| Impressão automática | Configura etiqueta e impressora e imprime os pedidos aprovados |
| Comunicação por arquivo | Cada robô monitora um arquivo do anterior, sem depender de nenhum ficar aberto o tempo todo |
| Configuração compartilhada | Os três robôs leem o mesmo `.env`, cada um usando apenas as variáveis de que precisa |

## ⋆˚✮ Destaques técnicos

- **Integração por arquivo** — a fila, o status do ciclo e o histórico de
  aprovação são o contrato entre os robôs; qualquer um pode ser aberto em
  qualquer ordem e espera o arquivo do anterior aparecer.
- **Aviso de fim de ciclo** — o Aprovador sinaliza o fim de cada ciclo, com
  sucesso ou não, e o Preparador libera a tela para o próximo lote.
- **Histórico versionado** — aprovação e impressão gravam o status de cada
  pedido em arquivos versionados por data e setor.
- **Seletores em JSON separado** — os XPaths do portal ficam fora do código e
  são recarregados a cada ciclo.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Uma pessoa escolhe a data e o setor no Preparador
│
├─ Preparador atualiza a consulta e entrega a fila de pedidos
│
├─ Aprovador detecta a fila e abre cada pedido no portal
│   ├─ Aprova os pedidos que estão de acordo com os critérios
│   └─ Sinaliza o fim do ciclo, e o Preparador libera a tela
│
└─ Uma pessoa escolhe data, setor, etiqueta e impressora na Impressão
    ├─ Impressão lê os pedidos aprovados do lote
    └─ Imprime cada pedido no portal e registra o status de cada um
```

### ✮ Pré-Requisitos

⋆˚✮ Os robôs dependem da rede corporativa, de planilhas internas e de um portal
web de pedidos. Não são executáveis fora desse ambiente, nem para teste:
publicado como peça de portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Execução dos robôs |
| Google Chrome + Chromedriver | Navegação no portal web (Aprovador e Impressão) |
| Microsoft Excel | Atualização da consulta de pedidos (Preparador) |
| Windows | Ambiente das automações |

### ✮ Configuração

⋆˚✮ A configuração real fica em `Config_Cg/.env` (não versionado),
compartilhado pelos três robôs. Referências em `Config_Cg/env.exemplo`.

## ⋆˚✮ Stack

`Python 3.10+` · `Selenium` · `pywin32 / win32com` · `openpyxl` ·
`customtkinter` · `pystray` · Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
