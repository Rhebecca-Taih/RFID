<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Aprovador%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Aprovador"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    Vigia a fila de pedidos preparada pelo Preparador; abre cada um no<br>
    portal web, confere artigo, quantidade e modelo, e aprova<br>
    automaticamente os que estão de acordo — com o mesmo rigor de uma<br>
    conferência manual, operando 24 horas por dia.
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

Segunda etapa do pipeline de aprovação de pedidos. Antes desta automação,
cada pedido de etiqueta RFID era aberto manualmente no portal do
fornecedor para verificar se o artigo e a quantidade correspondiam ao
planejado — um processo repetitivo, suscetível a erro humano, que atrasava
as etapas seguintes (impressão e envio) até a fila ser revisada por
completo.

O Aprovador automatiza essa etapa: processa a fila entregue pelo
Preparador, abre cada pedido no portal, compara artigo, quantidade e
modelo com o planejado, e aprova automaticamente os que estão de acordo —
ajustando a quantidade quando necessário, sem intervenção manual. Casos
ambíguos (pedido fracionado em mais de uma linha, ou com sinal de
inconsistência no portal) são encaminhados para revisão humana. Opera
continuamente, 24 horas por dia, com pausa noturna automática, e pode ser
retomado em qualquer máquina da rede.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Conferência automática | Compara artigo, quantidade e modelo do pedido entre a planilha e o portal |
| Aprovação no portal | Aprova diretamente no portal os pedidos que estão de acordo com os critérios |
| Ajuste de quantidade assistido | Edita a quantidade no portal quando a planilha diverge, completando as duas confirmações exigidas pelo portal |
| Detecção de pedido duplicado | Compara o status do item com o estágio real do pedido no portal; se divergem, isola o pedido para revisão manual |
| Revisão manual protegida | Pedidos com mais de uma linha, ou com sinais de inconsistência, sempre exigem revisão manual |
| Histórico versionado | Cria um histórico de aprovação por versão, separando ano/mês/dia e passando o status de cada pedido |
| Seletores configuráveis | Todos os seletores do portal ficam num arquivo JSON separado, recarregado a cada ciclo |

## ⋆˚✮ Destaques técnicos

- **Cliques atômicos via JavaScript** — localizar o elemento, rolar até a
  área visível e clicar acontecem num único comando, executado pelo
  próprio navegador. Elimina o intervalo entre localizar e clicar
  presente numa automação tradicional em três passos separados, intervalo
  em que a página pode se re-renderizar.
- **Retomada de ciclo** — se a sessão do navegador cai no meio de um lote
  longo, a próxima tentativa automática lê o resultado parcial já salvo e
  pula os pedidos já resolvidos, em vez de reprocessar a fila inteira.
- **Diagnóstico completo por falha** — cada erro no portal gera uma pasta
  própria (organizada por data) com captura de tela, HTML completo da
  página e um snapshot do JSON de seletores exatamente como estava
  carregado em memória naquele instante — evidência suficiente para
  ajustar o seletor sem precisar reproduzir o problema.
- **Seletores em camadas** — cada campo tem um XPath principal e um de
  reserva (por posição ou por texto visível). O robô continua o
  processamento e registra no log toda vez que usa a reserva, sinalizando
  qual seletor revisar primeiro na próxima manutenção.
- **Lock distribuído com heartbeat** — impede que duas máquinas processem
  o mesmo lote ao mesmo tempo; se a máquina ativa parar de responder por
  mais de duas horas, outra assume o processamento automaticamente.
- **Pausa noturna automática** — encerra às 20h e retoma automaticamente às 7h30.
- **Continuidade com a rede indisponível** — o ciclo principal é
  supervisionado e reiniciado após uma falha inesperada; enquanto a rede
  está inacessível, os registros seguem numa pasta local, e o log
  principal indica o período de indisponibilidade quando o acesso volta.
- **Auto-instalação** — dependências e cópia do Chrome/Driver da rede na
  primeira execução em cada máquina, com progresso visível na tela.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Detecta quando o Preparador entrega uma nova fila de pedidos
│
├─ Abre o navegador e entra no portal
├─ Navega até a lista de pedidos
│
├─ Processa cada pedido da fila
│   ├─ Confere status, artigo e quantidade no portal
│   │   ├─ Novo + artigo e quantidade corretos          → aprova no portal
│   │   ├─ Novo + planilha maior que o portal           → edita a quantidade e aprova
│   │   ├─ Novo + portal maior que a planilha           → atualiza a planilha, portal intacto
│   │   ├─ Novo + artigo divergente                     → reprova
│   │   ├─ Status já avançado                           → registra, sem reaprovar
│   │   └─ Mais de uma linha                            → revisão manual
│
├─ Grava um histórico de aprovação por versão, com o status de cada pedido
├─ Salva uma cópia do resultado para o robô de Impressão
│
└─ Sinaliza o fim do ciclo para o Preparador
```

### ✮ Pré-Requisitos

Este robô depende da rede corporativa e do portal de pedidos — não é
executável fora desse ambiente, nem para teste. Este repositório está
publicado como peça de portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Interpretador que executa o robô |
| Windows | Único sistema operacional suportado |
| Acesso à rede corporativa | Cópia do Chrome/Driver, portal de pedidos e planilhas compartilhadas |

As bibliotecas Python (`Selenium`, `customtkinter`...) são instaladas
automaticamente pelo robô na primeira execução — ver [Stack](#-stack).

### ✮ Configuração

⋆˚✮ A configuração real fica em `../Config_Cg/.env` (não versionado).
Referências em `../Config_Cg/env.exemplo`.

| Variável | O que controla |
| :--- | :--- |
| `CAMINHO_REDE_BIN` | Pasta de rede com Chrome/Driver, copiada para o PC na 1ª execução |
| `PORTAL_USER` / `PORTAL_SENHA` | Credenciais do portal de pedidos |
| `PORTAL_URL_LOGIN` | URL de login do portal |
| `PORTAL_SITE` | Site selecionado na tela após o login |

## ⋆˚✮ Stack

`Python 3.10+` · `Selenium` · `customtkinter` · `pystray` · `openpyxl` ·
Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<sub>Documentação técnica completa (guia de uso, arquitetura) em
[DOCUMENTACAO.md](./DOCUMENTACAO.md) · Licença em
[LICENSE](../../LICENSE)</sub>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
