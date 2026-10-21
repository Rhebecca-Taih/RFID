<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Base%20Geral%20%E2%80%94%20Documenta%C3%A7%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Base Geral — Documentação"/>

Manual de referência do robô de Base Geral: como operar no dia a dia e
como o sistema é construído por dentro. Complementa o
[README](./README.md), que apresenta o projeto em linhas gerais.

---

## ⋆˚✮ Guia de Uso

### ✮ Antes de iniciar

⋆˚✮ O ambiente precisa ter:

| Item | Por quê |
| :--- | :--- |
| Python instalado nesta máquina | O arquivo do robô (`.pyw`) é executado pelo Python — sem ele instalado, o duplo clique não abre nada |
| Arquivo `.env` configurado | Define credenciais, links de origem e o caminho da planilha de rede — sem ele o robô não sabe onde buscar nem onde gravar |
| Acesso à rede corporativa | É onde ficam a planilha BASE GERAL.xlsx, o backup e o histórico de exclusões |
| Login Microsoft ainda válido | O robô reaproveita a sessão salva no perfil do Chrome portátil; se o usuário da conta mudar, é preciso atualizar `LOGIN_EMAIL`/`LOGIN_SENHA` no `.env` e refazer o login manual (ver "Tela a tela" → Final) |

### ✮ Como iniciar

1. Acesse a pasta do robô: `Automação Base Geral/`.
2. Dê duplo clique no arquivo `BASE_GERAL_auto.pyw`.
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

**Tela 2 — Bin**
Confirma se a pasta local de binários (Chrome e Driver portáteis) existe
e, se necessário, copia da rede. Avança automaticamente.

**Tela 3 — Chrome e Driver**
Mostra se o Chrome e o Driver portáteis foram encontrados e se as
versões são compatíveis entre si. Se houver incompatibilidade, o aviso
fica visível, mas é possível continuar.

**Tela 4 — Último status**
Mostra a última linha registrada no histórico da execução anterior —
permite ver de relance se o robô fechou em sucesso ou erro da última vez.

**Tela 5 — Máquinas**
Mostra o nome desta máquina e quando foi a última vez que rodou o robô
aqui, além da lista de outras máquinas que já rodaram. É só informativo.

**Tela 6 — Integridade da Base Geral**
Abre a planilha BASE GERAL.xlsx da rede só para conferir se ela abre sem
erro. Se a planilha estiver corrompida e houver um backup disponível,
aparece o botão **Restaurar Backup**, que substitui o arquivo de rede
pela última cópia de segurança.

**Tela 7 — Final**
Resume o status da conferência e libera o botão **Iniciar**. Também
mostra o botão **Login Manual**, que abre o Chrome portátil para o
usuário entrar manualmente na conta Microsoft (necessário quando a
sessão expira ou o autenticador pede confirmação) — basta fazer login,
fechar o Chrome e depois clicar em Iniciar normalmente.

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
| Ver histórico | Abre uma janela com o histórico do dia, atualizada ao vivo |
| Status | Mostra o estado atual sem abrir nada (apenas informativo) |
| Parar robô | Encerra o processo e libera o controle de instância única |

**Janela de histórico ao vivo**
Mostra os blocos de log do dia, coloridos por tipo (sucesso, aviso,
erro), atualizada automaticamente conforme o robô registra eventos novos. O
botão "Abrir arquivo bruto" abre o `.txt` original no bloco de notas.

A cada 15 minutos, o robô baixa as duas planilhas de origem, compara com
a BASE GERAL.xlsx da rede e grava apenas o que mudou (itens novos,
atualizados ou excluídos). Das 20h às 8h, o robô entra em pausa noturna
e retoma automaticamente, sem precisar de ação manual.

### ✮ Como encerrar

Clique com o botão direito no ícone da bandeja e selecione **Parar robô**.
Fechar a janela do terminal sem usar essa opção pode deixar o controle de
instância única travado até a próxima verificação automática.

### ✮ Status do ciclo

Este robô não grava status por item — ele registra o resultado de cada
ciclo de sincronização no histórico. As mensagens mais relevantes:

| Mensagem | O que significa | O que fazer |
| :--- | :--- | :--- |
| BASE GERAL SINCRONIZADA COM SUCESSO | O ciclo terminou e a planilha de rede foi atualizada | Nenhuma |
| Sincronizacao abortada | Uma das duas planilhas de origem não foi baixada a tempo | O robô tenta de novo no próximo ciclo; se persistir, conferir o acesso ao link de origem |
| Aba [...] não sumiram da origem, mas NAO consegui salvar a copia de seguranca | Havia exclusões a aplicar, mas o histórico de exclusões não pôde ser gravado | Nenhuma exclusão foi aplicada neste ciclo, por segurança; conferir acesso à pasta de histórico na rede |
| ERRO ao gravar Excel | Falha durante a escrita na cópia temporária da planilha | A planilha de rede não é alterada nesse ciclo; o robô tenta de novo no próximo |
| PAUSA -- Encerramento automático | Início da pausa noturna | Nenhuma — retoma automaticamente no horário configurado |
| Rede indisponível de [início] até [fim] | A pasta de log na rede ficou inacessível nesse período | Nenhuma — os registros do período ficam na pasta local indicada na própria mensagem |
| O loop principal parou por um erro inesperado -- reiniciando | Uma falha inesperada interrompeu o ciclo, que foi reiniciado em seguida | Nenhuma, se não se repetir; se se repetir, consultar `logs/historico_erros.txt` |

⋆˚✮ O histórico de erros técnicos completo fica em
`logs/historico_erros.txt`, com data e hora de cada ocorrência, e as
alterações de dados linha a linha ficam em `logs/historico_mudancas.txt`
— use esses arquivos para investigar um problema que se repete.

---

## ⋆˚✮ Documentação Técnica

### ✮ Arquitetura

```text
Portal de origem (download via Selenium)
   ├─ CONTROLE EMISSÃO (planilha web)
   └─ Solicitação de Etiquetas (planilha web)
          │
          ▼
   Robô Base Geral
   compara cada aba com a BASE GERAL.xlsx da rede,
   calcula diferenças (novo / atualizado / excluído)
          │
          ▼
   BASE GERAL.xlsx (rede)
   ├─ PEDIDOS AGENDADOS
   ├─ PEDIDOS FORA DE AGENDA
   ├─ [categoria parceiro]
   └─ PEDIDOS FORA IMPRIMIR
```

Robô independente, sem relação de entrada/saída com os outros robôs do
repositório — ele alimenta a planilha de rede que serve de referência
para a operação, mas não lê nem escreve diretamente nas pastas dos
outros robôs.

### ✮ Módulos

#### ⋆ Controle de instância única

Antes de abrir a janela de lançamento, o robô grava um arquivo de lock
com PID, nome da máquina e um heartbeat atualizado a cada 10 minutos.
Outra máquina só é liberada para iniciar se o lock atual estiver há mais
de 2 horas sem atualização — evita duas máquinas sincronizando a mesma
planilha ao mesmo tempo.

#### ⋆ Login manual assistido

Além do login automático (usado no fluxo normal de download), a tela
final oferece um botão para abrir o Chrome portátil isoladamente, com o
mesmo perfil salvo usado pelos downloads. Permite ao usuário completar
manualmente etapas que o fluxo automático não resolve, como a
confirmação do autenticador.

#### ⋆ Download com nova tentativa

Baixa as duas planilhas de origem via Chrome headless, com até três
tentativas e tempos de espera crescentes entre elas. Ao final de cada
tentativa falha, reinicia o Chrome e o driver antes de tentar de novo.

#### ⋆ Normalização de dados

Converte valores lidos da planilha (texto, número, data) para um formato
único antes de comparar — evita que uma mesma informação escrita de
jeitos diferentes (espaços, maiúsculas, formato de data) seja tratada
como uma mudança real.

#### ⋆ Cálculo de diferenças (diff)

Compara cada linha da planilha de origem com a BASE GERAL.xlsx da rede
usando uma chave composta (pedido, artigo, data, mais um contador de
desempate), classificando cada linha como nova, atualizada ou removida.

#### ⋆ Histórico de exclusões versionado

Antes de remover qualquer linha da planilha de rede, salva uma cópia das
linhas que serão excluídas e, quando possível, uma cópia completa da
planilha antes da exclusão — organizadas por ano/mês/dia, com numeração
sequencial reservada de forma atômica.

#### ⋆ Escrita via Excel COM

Abre uma cópia temporária local da planilha de rede pelo Excel, aplica
todas as mudanças do ciclo (atualizações, inclusões, exclusões) e só
então substitui o arquivo de rede pelo resultado. As exclusões removem
apenas o intervalo de colunas da tabela principal de cada aba. Na aba
PEDIDOS FORA IMPRIMIR, a coluna de setor é preenchida com o setor da
Solicitação de Etiquetas; as colunas de fórmula e de preenchimento
manual não são alteradas.

#### ⋆ Histórico ao vivo

Lê o arquivo de log e separa em blocos, classificando cada um por tipo
(sucesso, aviso, erro) pela presença de palavras e símbolos específicos,
exibindo com cor própria na janela de histórico.

#### ⋆ Loop principal

Alterna entre executar um ciclo de sincronização e respeitar a pausa
noturna, atualizando o heartbeat do lock em intervalos regulares mesmo
durante a pausa.

#### ⋆ Continuidade com a rede indisponível

O loop principal executa sob supervisão: uma falha inesperada é
registrada e o loop é reiniciado após 30 segundos, sem encerrar o
processo. Quando a pasta de log na rede está inacessível, os registros
vão para uma pasta local da máquina (`%LOCALAPPDATA%\RobosBureau\Base Geral\`,
mantida por 30 dias); ao restabelecer o acesso, o log da rede recebe uma
linha com o período de indisponibilidade e a localização dos registros
locais.

### ✮ Decisões de Arquitetura

- **Edita uma cópia temporária local antes de substituir o arquivo de
  rede** — se o processo cair no meio da gravação, a planilha de rede
  nunca fica num estado parcialmente escrito; só é substituída depois
  que a cópia local termina com sucesso.
- **Salva uma cópia das linhas excluídas antes de aplicar qualquer
  exclusão, e cancela a exclusão daquele ciclo se não conseguir salvar**
  — uma exclusão em planilha não tem desfazer simples; a cópia de
  segurança existe antes da ação ser aplicada, não depois.
- **Desliga o AutoFilter antes de gravar ou apagar linhas** — um filtro
  ativo no Excel altera o índice real das linhas visíveis, o que faria o
  robô escrever ou apagar a linha errada.
- **Apaga linhas de baixo para cima** — remover de cima para baixo
  desloca o índice de todas as linhas seguintes, fazendo a próxima
  exclusão da lista atingir a linha errada.
- **Exclui apenas o intervalo da tabela principal, não a linha inteira da
  planilha** — preserva tabelas auxiliares que ocupam a mesma faixa de
  linhas em outras colunas, como a origem de listas suspensas.
- **Preenche a coluna de setor na aba PEDIDOS FORA IMPRIMIR** — a fórmula
  padrão dessa coluna depende do modelo, informação que só existe depois
  da impressão.
- **Registros alternam para uma pasta local quando a rede está
  indisponível** — o log fica na rede; o registro local preserva a
  sequência de eventos do período sem acesso e o processamento continua
  até o acesso voltar.
- **Usa o Chrome e o chromedriver portáteis, não os instalados no
  Windows** — o Chrome do sistema se atualiza automaticamente e pode ficar
  incompatível com a versão do driver; manter uma cópia própria evita
  que uma atualização externa quebre o robô sem aviso.
- **Reserva o número da próxima versão do histórico de exclusões de
  forma atômica (`O_EXCL`)** — evita que duas máquinas sincronizando ao
  mesmo tempo gravem o mesmo número de versão e sobrescrevam uma à
  outra.

### ✮ Configuração

⋆˚✮ Variáveis de ambiente usadas por este robô:

| Variável | O que controla |
| :--- | :--- |
| `LOGIN_EMAIL` / `LOGIN_SENHA` | Credenciais de login no portal de origem |
| `CAMINHO_REDE` | Caminho da planilha BASE GERAL.xlsx na rede |
| `LINK_EMISSAO` | Link da planilha web CONTROLE EMISSÃO |
| `LINK_ETIQUETAS` | Link da planilha web Solicitação de Etiquetas |
| `CAMINHO_REDE_BIN` | Pasta de rede com Chrome/Driver, copiada para o PC na 1ª execução |
| `NOME_ARQ_EMISSAO` / `NOME_ARQ_ETIQUETAS` | Padrão de nome usado para localizar o arquivo baixado |
| `CATEGORIA_PARCEIRO` | Nome da aba/categoria de parceiro tratada à parte das demais |
| `NOME_CRIADOR` / `LINK_GITHUB_CRIADOR` | Crédito de autoria exibido no cabeçalho da janela |

### ✮ Stack

`Python 3.10+` · `Selenium` · `pywin32 / win32com` · `pandas` ·
`openpyxl` · `customtkinter` · `pystray` · Somente Windows

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
