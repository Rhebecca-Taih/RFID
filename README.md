<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Automa%C3%A7%C3%A3o%20de%20Opera%C3%A7%C3%B5es%20RFID%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Automação de Operações RFID"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    Robôs em Python que automatizam, por etapas, o trabalho de um setor<br>
    inteiro de operações RFID, antes executado integralmente à mão.<br>
    Cada robô cobre uma parte do fluxo e entrega o trabalho ao próximo<br>
    por meio de arquivos.
  </samp>
</div>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=deaaf9" alt="Python" />
  <img src="https://img.shields.io/badge/Selenium-000000?style=for-the-badge&logo=selenium&logoColor=deaaf9" alt="Selenium" />
  <img src="https://img.shields.io/badge/Excel_·_win32com-000000?style=for-the-badge&logo=microsoftexcel&logoColor=deaaf9" alt="Excel / win32com" />
  <img src="https://img.shields.io/badge/Windows-000000?style=for-the-badge&logo=windows11&logoColor=deaaf9" alt="Windows" />
  <img src="https://img.shields.io/badge/status-finalizado-8323B5?style=for-the-badge" alt="Status: finalizado" />
</div>

<br>

## ⋆˚✮ Contexto

Um setor da cadeia de suprimentos operava inteiramente à mão: aprovação de
pedidos de etiqueta RFID num portal web, manutenção da base mestra de pedidos e
do histórico de indicadores, e a garantia de que os arquivos certos chegavam às
pastas de envio, tudo conferido e copiado manualmente, todos os dias. A
automação foi construída por etapas: cada robô cobre uma parte do fluxo, nenhum
precisa permanecer aberto o tempo todo, e qualquer máquina da rede retoma o
processamento de onde a anterior parou.

## ⋆˚✮ Funcionalidades

| Robô | Função |
| :--- | :--- |
| [**Base Geral**](Automa%C3%A7%C3%A3o%20Base%20Geral/) | Baixa os arquivos de origem (SharePoint e Google Sheets), cruza os dados e sincroniza a base mestra de pedidos, fonte dos indicadores do setor |
| [**Agendamento**](Automa%C3%A7%C3%A3o%20Agendamento/) | Mantém a versão mais recente do arquivo de agendamento na pasta de envio, sempre com nome fixo |
| [**Controle KPI**](Controle%20KPI%20OneDrive/) | Mantém os arquivos de indicadores atualizados em pastas sincronizadas pelo OneDrive, para o SharePoint refletir o dado mais recente |
| [**Preparador**](Rob%C3%B4s%20Bureau/Preparador/) | A partir de uma data e um setor, atualiza a consulta de pedidos, valida os fornecedores e entrega a fila pronta para a aprovação |
| [**Aprovador**](Rob%C3%B4s%20Bureau/Aprovador/) | Abre cada pedido da fila no portal web, confere artigo, quantidade e modelo, aprova os que estão de acordo e registra o status de cada um |
| [**Impressão**](Rob%C3%B4s%20Bureau/Impress%C3%A3o/) | Configura etiqueta e impressora e imprime no portal cada pedido aprovado, registrando o status de cada impressão |

⋆˚✮ Ideias não finalizadas, sem código publicado:

- **Finalizador**: enviar o resultado aprovado à planilha online oficial e
  manter um backup consolidado na rede.
- **Bip**: conferir no portal web os pedidos impressos de um lote e registrar o
  resultado da conferência de cada pedido.

## ⋆˚✮ Destaques técnicos

- **Lock distribuído com heartbeat**: apenas uma máquina executa um robô por
  vez; o lock expira automaticamente caso um computador trave sem liberá-lo.
- **Auto-instalação em tempo de execução**: em uma máquina nova, o robô instala
  as próprias dependências por trás de uma tela de progresso e copia o Chrome e o
  Chromedriver da rede na primeira execução.
- **Diagnóstico completo de falhas**: cada erro no portal gera uma pasta com
  captura de tela, o HTML da página, os seletores carregados e a exceção do
  Selenium, organizados por data e removidos após dez dias.
- **Seletores em arquivo JSON separado**: quando o portal muda, ajusta-se o
  JSON, não o código. Cada clique acontece num único comando JavaScript
  atômico (localizar, rolar até a vista e clicar).
- **Detecção de sessão encerrada**: se o navegador é finalizado durante um
  lote, o ciclo é interrompido, o resultado parcial é salvo e a nova tentativa
  continua do ponto em que parou.
- **Continuidade sem rede**: quando a pasta de rede fica indisponível, os robôs
  seguem gravando localmente e registram o período de indisponibilidade.
- **Pausa noturna**: encerra às 20h e retoma às 7h30, sem finalizar o processo.
- **Retentativa com backoff** em todo download e cópia de arquivo.
- **Aplicação na bandeja do sistema**, com janela de histórico em tempo real e
  tema escuro, construída em customtkinter.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Robôs de ciclo contínuo, ligados ao iniciar o dia
│
├─ Base Geral baixa os arquivos de origem, cruza os dados e atualiza a base mestra
├─ Agendamento detecta o arquivo de agendamento mais recente e o copia para a pasta de envio
└─ Controle KPI detecta mudanças nos arquivos de indicadores e atualiza as cópias sincronizadas

Esteira de pedidos, iniciada por uma pessoa
│
├─ Preparador recebe a data e o setor, atualiza a consulta e entrega a fila
├─ Aprovador abre cada pedido no portal, confere os critérios e aprova
│   └─ Avisa o fim do ciclo para o Preparador liberar a tela
└─ Impressão recebe data, setor, etiqueta e impressora e imprime os pedidos aprovados
    └─ Registra o status de cada pedido, organizado por data e setor
```

### ✮ Pré-Requisitos

⋆˚✮ Os robôs dependem da rede corporativa, de planilhas internas e de um portal
web de pedidos. Não são executáveis fora desse ambiente, nem para teste:
publicado como peça de portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Execução dos robôs |
| Google Chrome + Chromedriver | Navegação no portal web |
| Microsoft Excel | Atualização de consultas e planilhas via win32com |
| Windows | Ambiente das automações |

### ✮ Configuração

⋆˚✮ A configuração real de cada robô fica num `.env` (não versionado), na pasta
do robô ou em `Config_Cg/`. Referências em cada `env.exemplo`.

## ⋆˚✮ Stack

`Python 3.10+` · `Selenium` · `pywin32 / win32com` · `pandas` · `openpyxl` ·
`customtkinter` · `pystray` · Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
