<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Impress%C3%A3o%20%E2%80%94%20Documenta%C3%A7%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Impressão — Documentação"/>

Manual de referência do Robô de Impressão: como operar no dia a dia e
como o sistema é construído por dentro. Complementa o
[README](./README.md), que apresenta o projeto em linhas gerais.

---

## ⋆˚✮ Guia de Uso

### ✮ Antes de iniciar

⋆˚✮ O ambiente precisa ter:

| Item | Por quê |
| :--- | :--- |
| Python instalado nesta máquina | O arquivo do robô (`.pyw`) é executado pelo Python — sem ele instalado, o duplo clique não abre nada |
| Arquivo `.env` configurado | Define credenciais do portal, a base mestra de referência e a planilha auxiliar — sem ele o robô não sabe onde buscar nem como logar |
| Acesso à rede corporativa | Cópia do Chrome/Driver, portal de pedidos e base mestra de referência |
| Login do portal ainda válido | Credenciais compartilhadas com o Robô Aprovador; se o usuário mudar, atualizar `PORTAL_USER`/`PORTAL_SENHA` no `.env` |
| Lote já aprovado pelo Robô Aprovador | Este robô só processa o que já passou pela etapa de aprovação, para a Data/Setor escolhidos |

### ✮ Como iniciar

1. Acesse a pasta do robô: `Robôs Bureau/Impressão/`.
2. Dê duplo clique no arquivo `Robo_Impressao.pyw`.
3. A janela confere o ambiente automaticamente e abre a tela principal.
4. Escolha Data, Setor, Etiqueta e Impressora, depois clique em
   **Processar**.

Este robô não é executado em ciclo contínuo pela bandeja — processa um lote
por vez, sob comando manual, com a janela
aberta até o fim do ciclo.

### ✮ Tela a tela

**Tela inicial — Preparando o ambiente**
Quatro etapas, cada uma com o botão "Continuar":

1. **Bibliotecas** — confere cada biblioteca e instala automaticamente as que faltarem
   (✓ pronta, ✕ falhou, círculo girando enquanto instala).
2. **Pasta Bin** — copia o Chrome e o driver da rede (`CAMINHO_REDE_BIN`) na
   primeira vez em cada computador, com contador de tempo. Nas outras vezes
   mostra "Já existe localmente".
3. **Chrome e Driver** — confere se os dois estão no computador.
4. **Final** — "Tudo certo! Pronto para iniciar" e o botão **Iniciar**, que
   abre a tela principal. Se alguma etapa falhou, mostra o aviso e o botão
   **Reiniciar**.

**Tela principal — Data, Setor, Etiqueta e Impressora**
Campo de data (digitado ou escolhido num calendário) e botões para
escolher setor, modelo de etiqueta (com a opção **Detecção automática**,
que decide o modelo a partir dos dados do próprio pedido) e impressora. O
botão **Processar** só é liberado quando todos os campos estão
preenchidos.

**Tela excepcional — Essa Data/Setor foi processada recentemente**
Aparece quando o mesmo lote já foi processado há menos de 40 minutos —
proteção contra duas pessoas iniciarem o mesmo processamento quase ao
mesmo tempo sem saber uma da outra, o que duplicaria etiquetas.

**Tela — Processando**
Mostra que o robô está logando no portal e processando os pedidos do
lote. O botão **Parar** pede confirmação, deixa o pedido em andamento
terminar e para antes do próximo. O que já foi impresso fica salvo em
IMPRESSOS, e a tela mostra "Processo parado pelo usuário".

**Tela — Processamento concluído**
Resume o resultado do ciclo: total de pedidos do dia, quantos foram
aprovados, quantos foram efetivamente impressos, quantos já tinham sido
processados antes (para conferência) e quantos deram erro. Oferece
**Nova impressão** (volta à tela principal) ou reenviar a mesma
Data/Setor.

**Tela excepcional — Processamento não concluído**
Aparece em falhas não críticas (por exemplo, falha ao abrir o
navegador ou ao fazer login). Mostra o motivo e permite tentar de novo.

**Tela excepcional — Processo interrompido**
Aparece quando o robô detecta um problema sério no meio do lote (sessão
do navegador caiu, o agente de impressão parou de confirmar impressões,
ou o filtro de site do portal não resetou). Mostra quantos pedidos já
foram impressos até a parada e se o resultado parcial foi salvo.

### ✮ Uso no dia a dia

O fluxo típico é: abrir o robô, escolher Data/Setor/Etiqueta/Impressora,
clicar em Processar, e acompanhar o log pela tela ou pelo botão **Abrir
log**. Ao reenviar a mesma Data/Setor (botão "Imprimir novamente"),
qualquer pedido que já não esteja mais "NOVO" no portal é pulado
automaticamente — reenviar não duplica etiquetas já impressas.

### ✮ Como encerrar

Feche a janela normalmente a qualquer momento.

### ✮ Status por pedido

Cada pedido processado recebe um valor na coluna de status de impressão,
salvo no histórico versionado do dia:

| Status | O que significa | O que fazer |
| :--- | :--- | :--- |
| IMPRESSO | Impressão confirmada no portal com sucesso | Nenhuma |
| MOV (COM A EQUIPE, ATE 7 DIAS) | Pedido já tinha etiqueta impressa há até 7 dias, conforme a base mestra | Nenhuma |
| COLMEIA | Etiqueta física já disponível numa planilha auxiliar de estoque | Nenhuma |
| IMPRESSO AVULSO | Pedido sem etiqueta disponível em nenhuma fonte, impresso manualmente pelo fluxo de impressão avulsa | Nenhuma |
| VERIFICAR AVULSA | A impressão avulsa não conseguiu confirmar o resultado | Conferir o pedido manualmente no portal |
| AVULSO - SEM ARTIGO | O artigo do pedido não foi encontrado na tela de impressão avulsa | Conferir o pedido manualmente no portal |
| ERRO AO IMPRIMIR, VERIFICAR PEDIDO / ERRO AO IMPRIMIR AVULSA, VERIFICAR PEDIDO | A impressão não foi confirmada no portal | Conferir o pedido manualmente no portal |
| ARTIGO DIVERGENTE, NAO IMPRIMIR | O artigo do pedido diverge do esperado | Revisão manual antes de imprimir |
| URGENTE VERIFICAR PEDIDO NÃO ENCONTRADO NA BASE GERAL | O pedido não aparece na base mestra de referência | Verificar o pedido com urgência |

Pedidos que o portal já mostra com status diferente de "NOVO" ao abrir
são contados à parte, como "já processados antes" — mantidos como
estavam, sem gerar uma nova tentativa de impressão.

⋆˚✮ O histórico de erros técnicos completo fica em
`logs/historico_erros.txt`. Cada falha no portal também gera uma pasta
própria em `logs/ERRO/`, com captura de tela, HTML da página e um
registro dos seletores carregados naquele instante.

---

## ⋆˚✮ Documentação Técnica

### ✮ Arquitetura

```text
HISTORICO DE APROVAÇÃO (gravado pelo Robô Aprovador)
   │  lote de pedidos de uma Data/Setor
   ▼
Robô de Impressão
   ├─ Pedidos "APROVADO"      → configura Etiqueta/Impressora e imprime no portal
   └─ Pedidos MOV/qtd divergente → classifica contra a base mestra e a
                                    planilha auxiliar (Colmeia); o que
                                    sobrar vai para impressão avulsa
          │
          ▼
   IMPRESSOS (histórico versionado, por Data/Setor)
```

Lê a pasta de histórico que o Robô Aprovador grava, mas não escreve nela
— a integração é de leitura apenas. A base mestra de referência é lida
em cópia local somente leitura, nunca o arquivo de rede diretamente.

### ✮ Módulos

#### ⋆ Leitura do histórico de aprovação

Junta todas as versões de um dia/setor gravadas pelo Aprovador,
mesclando por número do pedido — a versão mais recente de cada pedido
prevalece.

#### ⋆ Classificação de pedidos MOV

Pedidos marcados como MOV ou com quantidade divergente pelo Aprovador
não são impressos de novo automaticamente: são conferidos contra a cópia
local da base mestra (já impressos há até 7 dias) e contra uma planilha
auxiliar pública (Colmeia), que lista etiquetas físicas já disponíveis
por setor. O que não se encaixa em nenhuma das duas fontes vai para a
impressão avulsa.

#### ⋆ Impressão normal (fila de Pendentes)

Para cada pedido aprovado, busca no portal, confere se o status ainda é
"NOVO", configura etiqueta e impressora e confirma a impressão — com
captura de diagnóstico completo (tela, HTML, seletores carregados)
sempre que uma etapa falha.

#### ⋆ Impressão avulsa

Fluxo separado para pedidos sem etiqueta disponível em nenhuma fonte.
Usa busca por texto/rótulo visível via JavaScript em vez dos seletores
configurados, porque essa tela do portal não tem a mesma estrutura
estável da fila de Pendentes.

#### ⋆ Reset do filtro de Site

Antes de cada busca de pedido, confere se o filtro de Site do portal
está limpo (mostrando todos os sites) e o reseta se necessário —
necessário porque o filtro às vezes retém o site do pedido anterior.

#### ⋆ Diagnóstico completo por falha

Cada erro no portal gera uma pasta própria (organizada por dia,
numerada sequencialmente) com captura de tela, HTML da página e um
snapshot do JSON de seletores exatamente como estava carregado em
memória naquele instante.

#### ⋆ Histórico versionado

Salva o resultado de cada ciclo como uma nova versão numerada, por
Data/Setor — nunca sobrescreve uma versão anterior.

#### ⋆ Registro local com a rede indisponível

Quando a pasta de log na rede está inacessível, os registros vão para
uma pasta local da máquina (`%LOCALAPPDATA%\RobosBureau\Impressao\`,
mantida por 30 dias); ao restabelecer o acesso, o log da rede recebe uma
linha com o período de indisponibilidade e a localização dos registros
locais.

### ✮ Decisões de Arquitetura

- **Nunca abre o arquivo de rede da base mestra diretamente, só uma
  cópia local** — outro robô (Base Geral) pode estar escrevendo nesse
  mesmo arquivo ao mesmo tempo; ler a cópia evita disputa de acesso.
- **Interrompe o ciclo inteiro após falhas de impressão seguidas, em vez
  de continuar tentando pedido por pedido** — várias falhas seguidas
  normalmente indicam um problema no agente/software de impressão, não
  no pedido em si; continuar tentando desperdiçaria o restante do lote
  com o mesmo problema.
- **Usa um limite menor de falhas seguidas quando nenhum pedido ainda
  foi impresso com sucesso no ciclo** — nesse caso a origem do problema é
  ainda mais provável de ser o agente de impressão (não um pedido
  específico), então vale interromper mais cedo.
- **Reenviar a mesma Data/Setor pula pedidos que não estão mais "NOVO"
  no portal** — o status no portal é a fonte da verdade sobre o que já
  foi impresso; reenviar não duplica etiquetas já confirmadas.
- **Bloqueia reprocessar a mesma Data/Setor por 40 minutos** — cobre o
  caso de duas pessoas iniciarem o mesmo processamento quase ao mesmo
  tempo, sem saber uma da outra, o que duplicaria etiquetas físicas.
- **A impressão avulsa busca elementos por texto/rótulo visível, não por
  XPath configurado** — essa tela do portal não tem a mesma estrutura
  estável da fila de Pendentes; buscar pelo que o usuário vê na tela é
  mais resistente a mudanças de layout ali.
- **Registros alternam para uma pasta local quando a rede está
  indisponível** — o log fica na rede; o registro local preserva a
  sequência de eventos do período sem acesso e o processamento continua
  até o acesso voltar.

### ✮ Configuração

⋆˚✮ Variáveis de ambiente usadas por este robô:

| Variável | O que controla |
| :--- | :--- |
| `PORTAL_USER` / `PORTAL_SENHA` | Credenciais do portal de pedidos (compartilhadas com o Aprovador) |
| `PORTAL_URL_LOGIN` | URL de login do portal |
| `PORTAL_SITE` | Site selecionado na tela após o login |
| `CAMINHO_REDE_BIN` | Pasta de rede com Chrome/Driver, copiada para o PC na 1ª execução |
| `CAMINHO_REDE_BASE_GERAL` | Caminho de rede da base mestra de referência |
| `LINK_COLMEIA_ARTIGOS` | Link da planilha auxiliar pública com etiquetas físicas disponíveis |
| `SETORES_PREPARADOR` | Lista de setores disponíveis para seleção |
| `MODELOS_ETIQUETA_IMPRESSAO` / `IMPRESSORAS_DISPONIVEIS` | Opções disponíveis na tela |
| `NOME_CRIADOR` / `LINK_GITHUB_CRIADOR` | Crédito de autoria exibido no cabeçalho da janela |

### ✮ Stack

`Python 3.10+` · `Selenium` · `customtkinter` · `openpyxl` ·
Somente Windows

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
