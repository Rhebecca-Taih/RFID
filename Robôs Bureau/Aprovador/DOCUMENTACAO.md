<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Rob%C3%B4%20Aprovador%20%E2%80%94%20Documenta%C3%A7%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Robô Aprovador — Documentação"/>

Manual de referência do Robô Aprovador: como operar no dia a dia e como o
sistema é construído por dentro. Complementa o [README](./README.md), que
apresenta o projeto em linhas gerais.

---

## ⋆˚✮ Guia de Uso

### ✮ Antes de iniciar

⋆˚✮ O ambiente precisa ter:

| Item | Por quê |
| :--- | :--- |
| Python instalado nesta máquina | O arquivo do robô (`.pyw`) é executado pelo Python — sem ele instalado, o duplo clique não abre nada |
| Arquivo `.env` configurado | Guarda usuário, senha e endereço do portal — sem ele o robô não consegue fazer login |
| Login do portal (`PORTAL_USER`/`PORTAL_SENHA`) ainda válido | Se a conta de origem mudar ou for desativada, o login passa a falhar — atualizar essas duas variáveis no `.env` sempre que o usuário do portal mudar |
| Acesso à pasta de rede com Chrome/Driver | Usada na primeira execução em cada máquina, para copiar o navegador portátil localmente |
| Planilha `Fila_Aprovacao.xlsx` acessível | É o gatilho do robô — sem ela, não há o que processar |

### ✮ Como iniciar

1. Acesse a pasta do robô: `Robôs Bureau/Aprovador/`.
2. Dê duplo clique no arquivo `Robo_Aprovacao.pyw`.
3. A janela de lançamento abre automaticamente e percorre pelas telas descritas
   abaixo, na ordem.
4. Na última tela, clique em **Iniciar**.
5. A janela fecha e o robô segue em execução pela bandeja do sistema (ícone
   próximo ao relógio, no canto da tela).

### ✮ Tela a tela

**Tela 1 — Bibliotecas**
Confere se as bibliotecas necessárias já estão instaladas nesta máquina e
instala automaticamente o que faltar. Avança automaticamente ao concluir —
nenhuma ação necessária.

**Tela 2 — Bin (Chrome/Driver)**
Confere se o navegador portátil usado pelo robô já existe nesta máquina;
copia da rede se for a primeira vez. Pode levar alguns minutos nesse
caso — aguardar sem fechar a janela.

**Tela 3 — Chrome e Driver**
Confirma que as duas partes copiadas na tela anterior foram encontradas e
são compatíveis entre si. Só conferência, nenhuma ação necessária.

**Tela 4 — Final**
Resume o status da conferência e libera o botão **Iniciar**. Clicar nele
inicia o robô de fato.

**Tela excepcional — Robô já ativo em outra máquina**
Aparece no lugar das telas acima quando outra máquina já está executando
este robô no momento. Só fechar a janela — não é possível iniciar uma
segunda instância ao mesmo tempo.

### ✮ Uso no dia a dia

**Ícone na bandeja do sistema**
Depois de iniciado, o robô fica disponível pelo ícone na bandeja do
sistema (canto da tela, perto do relógio). Clicar com o botão direito
abre o menu de atalhos:

| Opção | Efeito |
| :--- | :--- |
| Abrir log | Abre o arquivo de histórico do dia em um editor de texto |
| Status | Mostra o estado atual sem abrir nada (apenas informativo) |
| Parar robô | Encerra o processo e libera o controle de instância única |

O robô observa a planilha `Fila_Aprovacao.xlsx` continuamente. Qualquer
atualização nela dispara um novo ciclo de processamento automaticamente —
não é preciso reiniciar o robô para cada lote. Das 20h às 7h30, o robô
entra em pausa noturna e retoma automaticamente, sem precisar de ação manual.

### ✮ Como encerrar

Clique com o botão direito no ícone da bandeja e selecione **Parar robô**.
Fechar a janela do terminal sem usar essa opção pode deixar o controle de
instância única travado até a próxima verificação automática.

### ✮ Status do ciclo

Além do status por pedido (abaixo), o robô sinaliza o resultado do
**lote inteiro** em `status_aprovador.txt`, que o Robô Preparador lê para
saber se pode seguir ou se precisa de atenção:

| Status do ciclo | Quando acontece | O que fazer |
| :--- | :--- | :--- |
| `OK` | O ciclo rodou do início ao fim sem falha de automação | Nenhuma |
| `ATENCAO` | Alguma falha impediu a execução completa do ciclo (navegador não abriu, login falhou, navegação até a tela de pedidos falhou, ou o navegador morreu repetidamente) | Consultar o log do robô; o Preparador mostra esse estado como "Aprovador deu erro" |

### ✮ Status por pedido

Ao final de cada pedido processado, o robô grava um status na coluna
`STATUS` da planilha de resultado. A tabela abaixo cobre todos os valores
que o sistema produz:

| Status | O que significa | O que fazer |
| :--- | :--- | :--- |
| `FORA CDA` | O pedido não é de impressão local CDA — fora do escopo deste robô | Nenhuma — segue o fluxo próprio desses pedidos, fora deste robô |
| `APROVADO` | Pedido conferido e aprovado no portal nesse ciclo | Nenhuma — segue para a impressão |
| `APROVADO COM QTD ALTERADA` | Quantidade do portal era maior que a da planilha; a planilha foi atualizada para refletir o portal | Nenhuma — segue para a impressão |
| `APROVADO COM QTD DO SITE ALTERADA` | Quantidade do portal era menor; o robô ajustou o portal para corresponder à planilha | Nenhuma — segue para a impressão |
| `MOV` | Pedido já estava em outra etapa do fluxo do portal, fora do controle deste robô | Nenhuma — o Robô de Impressão reavalia automaticamente (recência, Colmeia ou impressão avulsa) antes de precisar de revisão |
| `PEDIDO JA APROVADO ANTES MAS QTD DIVERGENTE` | Pedido já processado, mas a quantidade do portal é menor que a esperada | Nenhuma — o Robô de Impressão reavalia automaticamente (recência, Colmeia ou impressão avulsa) antes de precisar de revisão |
| `REPROVADO` | Artigo do portal não corresponde ao da planilha | Revisão manual — conferir o cadastro do artigo |
| `NAO ACHOU` | Pedido não apareceu na lista do portal após a busca | Confirmar se o número do pedido está correto na planilha |
| `MULTIPLAS LINHAS - REVISAR MANUAL` | A busca retornou mais de um resultado para o mesmo pedido | Revisão manual no portal |
| `PEDIDO COM STATUS DIFERENTES NO SITE, DUPLICADO` | O pedido aparece com status inconsistente entre o item e o cabeçalho, indício de duplicidade no portal | Revisão manual no portal |
| `ERRO BUSCA` | O campo de busca do portal não respondeu | Tentar novamente no próximo ciclo; se persistir, conferir o portal manualmente |
| `ERRO DETALHES` | Não foi possível carregar os itens do pedido | Tentar novamente no próximo ciclo |
| `ERRO LAPIS` / `ERRO EDITAR QTD` | Não foi possível abrir ou confirmar a edição de quantidade no portal | Revisão manual no portal |
| `ERRO APROVAR` | O botão de aprovação não respondeu | Revisão manual no portal |
| `PEDIDO CORRETO, ERRO AO ALTERAR QTD, VERIFICAR` / `PEDIDO CORRETO, ERRO AO APROVAR, VERIFICAR` | A ação foi enviada, mas o portal não confirmou o resultado esperado | Conferir o estado real do pedido diretamente no portal |
| `ERRO` | Falha inesperada durante o processamento do pedido | Conferir o histórico de erros; tentar novamente no próximo ciclo |

⋆˚✮ Se aparecer um status fora desta tabela, ou o robô sinalizar erro
crítico: cada falha de automação gera uma pasta numerada dentro de
`logs/ERRO/<ano>/<mês>/<dia>`, com print da tela, HTML da página e um
registro técnico do momento exato da falha — use esse material para
diagnosticar o caso antes de reportar.

---

## ⋆˚✮ Documentação Técnica

### ✮ Arquitetura

O Aprovador é a etapa intermediária de um fluxo com três robôs:

```text
Preparador
   │  grava
   ▼
Fila_Aprovacao.xlsx ──────────────┐
                                   │
                              Robô Aprovador
                                   │
                    ┌──────────────┼──────────────────┐
                    ▼              ▼                   ▼
          Resultado_Aprovacao   status_aprovador.txt   Histórico de Aprovação
          .xlsx (↓ Impressão)   (↑ Preparador)          (cópia mensal local)
```

- **Entrada**: `Fila_Aprovacao.xlsx`, entregue pelo Robô Preparador.
- **Saída processada**: `Resultado_Aprovacao.xlsx`, lida pelo Robô de
  Impressão.
- **Sinal de conclusão**: `status_aprovador.txt`, lido pelo Robô
  Preparador para saber quando o lote terminou.
- **Histórico interno**: cópia mensal de pedidos aprovados, usada para
  evitar duplicidade em reprocessamentos.

Essas três trocas de arquivo são contratos entre robôs independentes —
mudar o caminho de qualquer uma delas exige atualizar o robô do outro
lado também.

### ✮ Módulos

#### ⋆ Controle de instância única

Antes de abrir a janela de lançamento, o robô grava um arquivo de lock
com PID, nome da máquina e um heartbeat atualizado a cada 10 minutos.
Outra máquina só é liberada para iniciar se o lock atual estiver há mais
de 2 horas sem atualização (indício de que o processo anterior travou ou
a máquina caiu) — isso evita duas máquinas processarem a mesma fila ao
mesmo tempo.

#### ⋆ Login e navegação

Autentica no portal e navega até a tela de pedidos. Tenta duas vezes antes
de desistir, com tempo de espera maior na segunda tentativa.

#### ⋆ Filtro de site

Garante que a lista de pedidos não esteja filtrada por um site específico
antes de buscar um pedido — um filtro ativo esconderia pedidos de outros
sites da busca.

#### ⋆ Validação de pedido

Confere o pedido encontrado contra a planilha: artigo (confirma que é o
mesmo produto) e quantidade (compara o que está agendado com o que o
portal mostra).

#### ⋆ Ajuste de quantidade

Quando a quantidade diverge, decide a direção do ajuste: se a planilha
pede mais do que o portal tem, edita a quantidade no próprio portal; se o
portal já tem mais do que o agendado, atualiza a planilha para refletir o
portal. Nunca os dois ao mesmo tempo.

#### ⋆ Aprovação e confirmação

Aciona a aprovação no portal e confere se o status realmente mudou para
aprovado antes de considerar o pedido concluído — a ação de clicar não é
suficiente por si só, e o robô relê o status depois de clicar.

#### ⋆ Histórico de aprovações

Mantém uma cópia mensal dos pedidos aprovados, usada para não duplicar
registro quando a mesma fila é reprocessada (por exemplo, depois que o
navegador morreu e o ciclo foi retomado).

#### ⋆ Ciclo de processamento

Percorre a fila inteira, acompanha o progresso, e tolera a sessão do
navegador morrer no meio do ciclo — reabre um navegador novo e retoma
automaticamente, com um número limitado de tentativas antes de desistir
e sinalizar atenção para o ciclo inteiro.

#### ⋆ Diagnóstico

Captura print de tela, HTML da página e contexto técnico sempre que uma
ação de automação falha, organizados por data em `logs/ERRO/`.

#### ⋆ Continuidade com a rede indisponível

O loop principal executa sob supervisão: uma falha inesperada é
registrada e o loop é reiniciado após 30 segundos, sem encerrar o
processo. Quando a pasta de log na rede está inacessível, os registros
vão para uma pasta local da máquina (`%LOCALAPPDATA%\RobosBureau\Aprovador\`,
mantida por 30 dias); ao restabelecer o acesso, o log da rede recebe uma
linha com o período de indisponibilidade e a localização dos registros
locais.

### ✮ Decisões de Arquitetura

- **XPaths em um arquivo JSON externo, não no código** — o seletor de
  cada elemento do portal fica em `xpaths_aprovador.json`. Se o layout do
  portal mudar, ajusta-se esse arquivo sem precisar editar nem reiniciar
  o código do robô.
- **Chrome e Driver portáteis, copiados da rede, em vez do Chrome
  instalado no Windows** — evita depender de uma instalação que se atualiza
  automaticamente (o que quebraria a compatibilidade com a versão do Driver a
  qualquer momento, fora do controle do robô).
- **Retry limitado quando o navegador morre, não infinito** — depois de
  um número fixo de tentativas automáticas, o robô para e sinaliza
  atenção para o ciclo, em vez de tentar indefinidamente sem avisar ninguém.
- **Dois canais de status, não um só** — o status por pedido (na
  planilha) registra o resultado de cada item; o status do ciclo (no
  `status_aprovador.txt`) registra se o lote inteiro rodou sem problema
  de automação. São perguntas diferentes: "esse pedido foi aprovado?" e
  "o ciclo foi executado até o fim?".
- **Diagnóstico automático em vez de falha silenciosa** — toda falha de
  automação gera print, HTML e contexto técnico numa pasta própria, para
  que o problema possa ser investigado depois, sem precisar reproduzi-lo
  ao vivo.
- **Registros alternam para uma pasta local quando a rede está
  indisponível** — o log fica na rede; o registro local preserva a
  sequência de eventos do período sem acesso e o processamento continua
  até o acesso voltar.

### ✮ Configuração

⋆˚✮ Variáveis de ambiente usadas por este robô:

| Variável | O que controla |
| :--- | :--- |
| `PORTAL_USER` / `PORTAL_SENHA` | Credenciais de login no portal |
| `PORTAL_URL_LOGIN` | Endereço da tela de login |
| `PORTAL_SITE` | Site selecionado após o login |
| `CAMINHO_REDE_BIN` | Pasta de rede com o Chrome/Driver portáteis |
| `NOME_CRIADOR` / `LINK_GITHUB_CRIADOR` | Crédito de autoria exibido no cabeçalho da janela |

### ✮ Stack

`Python 3.10+` · `Selenium` · `openpyxl` · `customtkinter` · `pystray` ·
Somente Windows

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
