<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Base%20Geral%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Base Geral"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    Sincroniza automaticamente as planilhas de origem com a base mestra<br>
    de pedidos na rede — sem duplicar, sem perder atualização, sem<br>
    depender de conferência manual.
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

A base mestra de pedidos alimenta os indicadores do setor e precisa
refletir, o mais próximo possível do tempo real, o que está nas planilhas
de origem do SharePoint e do Google Sheets. Este robô automatiza essa
sincronização, em ciclo contínuo.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Download automático das origens | Baixa os arquivos de Controle de Emissão e Solicitação de Etiquetas a cada ciclo |
| Sincronização sem duplicar | Compara pedido a pedido e só atualiza, adiciona ou ignora conforme o caso |
| Exclusão segura | Remove da base um pedido que já não existe mais na origem, sempre com cópia de segurança prévia |
| Classificação automática por aba | Direciona cada pedido para a aba certa da base conforme o motivo e a categoria |
| Pausa noturna | Encerra e retoma automaticamente, sem intervenção manual |

## ⋆˚✮ Destaques técnicos

- **Exclusão segura** — antes de remover um pedido que sumiu da origem,
  salva uma cópia da lista de excluídos e uma cópia completa da base como
  estava, versionadas por dia; se essa cópia de segurança falhar, nada é
  excluído naquele ciclo.
- **Retentativa com espera crescente** — até três tentativas de download
  por arquivo de origem, com intervalo maior a cada nova tentativa.
- **Classificação isolada por aba** — leitura e gravação de cada aba da
  base acontecem em blocos independentes; uma falha numa aba não
  interrompe a sincronização das outras.
- **Continuidade com a rede indisponível** — o ciclo principal é
  supervisionado e reiniciado após uma falha inesperada; enquanto a rede
  está inacessível, os registros seguem numa pasta local, e o log
  principal indica o período de indisponibilidade quando o acesso volta.
- **Auto-instalação** — dependências e cópia do Chrome/Driver da rede na
  primeira execução em cada máquina, com progresso visível na tela.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Inicia um novo ciclo automaticamente, em intervalo fixo
│
├─ Baixa os arquivos de origem
│
├─ Lê e limpa os dados (espaços, formatos, datas)
├─ Compara pedido a pedido (chave: Pedido + Artigo + Data)
│   ├─ Existe e mudou   → atualiza a linha
│   ├─ Não existe       → adiciona no final
│   ├─ Existe e igual   → ignora
│   └─ Sumiu da origem  → remove da base, com cópia de segurança prévia
│
├─ Classifica cada pedido na aba certa
│   ├─ Controle de Emissão              → PEDIDOS AGENDADOS
│   ├─ Etiquetas, motivo padrão         → PEDIDOS FORA DE AGENDA
│   ├─ Etiquetas, categoria do parceiro → aba do parceiro logístico
│   └─ Etiquetas, sem impressão         → PEDIDOS FORA IMPRIMIR
│
└─ Grava na base mestra via Excel (arquivo temporário → rede)
```

### ✮ Pré-Requisitos

Este robô depende da rede corporativa e das planilhas de origem — não é
executável fora desse ambiente, nem para teste. Este repositório está
publicado como peça de portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Interpretador que executa o robô |
| Windows | Único sistema operacional suportado |
| Acesso à rede corporativa | Cópia do Chrome/Driver e gravação da base mestra final |

### ✮ Configuração

⋆˚✮ A configuração real fica em `.env` (não versionado). Referências em
`env.exemplo`.

| Variável | O que controla |
| :--- | :--- |
| `LOGIN_EMAIL` / `LOGIN_SENHA` | Login de acesso às planilhas de origem |
| `CAMINHO_REDE` | Caminho de rede da base mestra final |
| `LINK_EMISSAO` / `LINK_ETIQUETAS` | Links dos arquivos de origem |
| `NOME_ARQ_EMISSAO` / `NOME_ARQ_ETIQUETAS` | Nomes esperados dos arquivos baixados |
| `CATEGORIA_PARCEIRO` | Aba/categoria do parceiro logístico especial |
| `CAMINHO_REDE_BIN` | Pasta de rede com Chrome/Driver, copiada para o PC na 1ª execução |

## ⋆˚✮ Stack

`Python 3.10+` · `Selenium` · `pywin32 / win32com` · `pandas` ·
`openpyxl` · `customtkinter` · `pystray` · Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
