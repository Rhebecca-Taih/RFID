<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Preparador%20%E2%80%94%20Documenta%C3%A7%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Preparador — Documentação"/>

Manual de referência do robô Preparador: como operar no dia a dia e como
o sistema é construído por dentro. Complementa o
[README](./README.md), que apresenta o projeto em linhas gerais.

---

## ⋆˚✮ Guia de Uso

### ✮ Antes de iniciar

⋆˚✮ O ambiente precisa ter:

| Item | Por quê |
| :--- | :--- |
| Python instalado nesta máquina | O arquivo do robô (`.pyw`) é executado pelo Python — sem ele instalado, o duplo clique não abre nada |
| Arquivo `.env` configurado | Define os setores disponíveis e o caminho da planilha de fornecedores — sem ele o robô usa valores padrão |
| Acesso à rede corporativa | É onde ficam a planilha de query, a pasta do Aprovador (fila e status) e a planilha de fornecedores |
| Login Microsoft/Excel ainda válido | A atualização da query depende de uma sessão válida nas fontes de dados ligadas à planilha; se o usuário mudar, pode ser preciso reautenticar no Excel |

### ✮ Como iniciar

1. Acesse a pasta do robô: `Robôs Bureau/Preparador/`.
2. Dê duplo clique no arquivo `Robo_Preparador.pyw`.
3. A janela abre e confere o ambiente automaticamente (tela descrita
   abaixo). Ao concluir, mostra a tela principal.
4. Escolha a data do pedido e o setor, depois clique em **Processar**.

O Preparador não é executado em ciclo contínuo pela bandeja do sistema — ele
processa um lote por vez,
sob comando manual, e permanece com a janela aberta até o lote terminar.

### ✮ Tela a tela

**Tela inicial — Bibliotecas**
Confere se as bibliotecas necessárias já estão instaladas nesta máquina e
instala automaticamente o que faltar. Avança automaticamente para a tela
principal ao concluir.

**Tela principal — Data do pedido e Setor**
Campo de data (digitado ou escolhido num calendário) e botões para
escolher o setor do lote. O botão **Processar** só é liberado quando
ambos estão preenchidos.

**Tela excepcional — Já existe um lote em andamento**
Aparece quando já há um processamento em curso (nesta ou em outra
máquina). Mostra em qual máquina, desde quando, para qual data e setor —
e permite verificar novamente.

**Tela — Processando**
Mostra que a query está sendo atualizada no Excel. Etapa automática, sem
ação necessária.

**Tela excepcional — Fornecedores não mapeados**
Aparece quando a query encontra fornecedores sem classificação CDA/FORA
CDA na planilha de mapeamento. Lista os fornecedores pendentes e oferece
um atalho para abrir a planilha de fornecedores, corrigir manualmente e
então clicar em **Corrigi, atualizar** para refazer a query.

**Tela — Aguardando aprovação**
Mostra um cronômetro desde o envio do lote para o Robô Aprovador. O
botão **Seguir mesmo assim** permite avançar manualmente sem esperar a
confirmação automática, para os casos em que o Aprovador está demorando
ou foi encerrado manualmente.

**Tela — Aprovação concluída**
Confirma que o Aprovador sinalizou sucesso para esse lote. Oferece
**Processar nova data** (volta à tela principal) ou **Processar mesma
data novamente** (reenvia o mesmo arquivo preparado direto ao Aprovador,
sem atualizar a query de novo — pede confirmação antes).

**Tela excepcional — Erro no Aprovador**
Aparece quando o Robô Aprovador sinaliza um problema no lote. Mostra o
motivo relatado e oferece as mesmas opções da tela de conclusão.

### ✮ Uso no dia a dia

O fluxo típico é: abrir o robô, escolher data e setor, clicar em
Processar, e acompanhar o histórico ao vivo na própria janela até a tela
de conclusão aparecer. O histórico mostra cada etapa (atualização da
query, validação, cópia para a fila do Aprovador) conforme acontece.

### ✮ Como encerrar

Feche a janela normalmente. Se o fechamento ocorrer durante o
processamento ou a espera pela aprovação, o robô pede confirmação,
avisando que o Robô Aprovador continuará seu próprio processamento
independentemente. Se fechar durante a revisão de fornecedores
pendentes, nada terá sido enviado ainda ao Aprovador.

---

## ⋆˚✮ Documentação Técnica

### ✮ Arquitetura

```text
Planilha de query (Excel, fontes de dados ligadas)
   │  usuário informa data + setor
   ▼
Robô Preparador
   ├─ Atualiza a query e valida o resultado
   ├─ Verifica se todos os fornecedores estão mapeados (CDA / FORA CDA)
   └─ Copia o resultado para a fila do Robô Aprovador
          │
          ▼
   Fila_Aprovacao.xlsx (pasta do Aprovador)
          │
          ▼
   Robô Aprovador grava status_aprovador.txt ao concluir
          │
          ▼
   Preparador detecta o novo status e exibe o resultado
```

Este robô escreve diretamente na pasta do Aprovador (fila e arquivo de
status) e monitora esse mesmo arquivo para saber quando o lote foi
processado — é o único ponto de integração direta entre os dois robôs.

### ✮ Módulos

#### ⋆ Controle de instância única

Antes de processar um lote, grava um arquivo de lock com PID, nome da
máquina, data/hora de início, heartbeat, e também a data e o setor do
lote em andamento — permite informar ao usuário exatamente qual lote
está bloqueando um novo processamento.

#### ⋆ Atualização da query via Excel COM

Abre a planilha de query, insere a data e o setor nas células de
configuração, desliga a atualização em segundo plano das conexões (para
aguardar o resultado de forma síncrona) e dispara a atualização de todas
as fontes de dados ligadas.

#### ⋆ Validação do resultado da query

Depois de atualizar, confere se a data e o setor realmente aplicados na
planilha correspondem ao que foi solicitado — evita prosseguir com um
resultado desatualizado ou de outro lote.

#### ⋆ Verificação de fornecedores mapeados

Cada linha do resultado recebe uma classificação (CDA ou FORA CDA) via
fórmula. Se alguma linha não cair em nenhuma das duas categorias, o
fornecedor correspondente está sem mapeamento — o robô interrompe e pede
correção manual antes de prosseguir.

#### ⋆ Cópia para a fila do Aprovador

Copia o arquivo de query já atualizado e validado para a pasta do
Aprovador, onde ele é lido como fila de pedidos a processar.

#### ⋆ Espera pela confirmação do Aprovador

Depois de copiar o arquivo, monitora o arquivo de status do Aprovador
comparando a data de modificação com um snapshot tirado antes do envio —
só considera o resultado quando o arquivo for modificado depois desse
instante, evitando ler um status antigo de um lote anterior.

#### ⋆ Registro local com a rede indisponível

Quando a pasta de log na rede está inacessível, os registros vão para
uma pasta local da máquina (`%LOCALAPPDATA%\RobosBureau\Preparador\`,
mantida por 30 dias); ao restabelecer o acesso, o log da rede recebe uma
linha com o período de indisponibilidade e a localização dos registros
locais.

### ✮ Decisões de Arquitetura

- **Não é executado em ciclo contínuo pela bandeja** —
  este processo depende de uma decisão humana por lote (qual data, qual
  setor), então fica em primeiro plano até o usuário decidir avançar.
- **Compara a data de modificação do arquivo de status, não só sua
  existência** — o arquivo de status do Aprovador pode já existir de um
  lote anterior; comparar o timestamp evita que o Preparador leia um
  resultado desatualizado como se fosse do lote atual.
- **Pede confirmação ao fechar durante processamento ou espera** — o
  Robô Aprovador continua seu próprio ciclo independente mesmo se o
  Preparador for fechado; o aviso existe para deixar isso explícito ao
  usuário antes de fechar.
- **Oferece "Seguir mesmo assim" na tela de espera** — cobre o caso em
  que o Aprovador foi encerrado manualmente ou está demorando além do
  esperado, sem travar o Preparador numa espera indefinida.
- **Verifica fornecedores mapeados antes de copiar para a fila, não
  depois** — um fornecedor sem classificação correta chegaria ao
  Aprovador com informação ambígua; a verificação acontece enquanto
  ainda é possível corrigir a planilha de origem.
- **Registros alternam para uma pasta local quando a rede está
  indisponível** — o log fica na rede; o registro local preserva a
  sequência de eventos do período sem acesso e o processamento continua
  até o acesso voltar.

### ✮ Configuração

⋆˚✮ Variáveis de ambiente usadas por este robô:

| Variável | O que controla |
| :--- | :--- |
| `SETORES_PREPARADOR` | Lista de setores disponíveis para seleção (separados por vírgula) |
| `CAMINHO_FORNECEDORES` | Caminho da planilha de mapeamento de fornecedores |
| `NOME_CRIADOR` / `LINK_GITHUB_CRIADOR` | Crédito de autoria exibido no cabeçalho da janela |

### ✮ Stack

`Python 3.10+` · `pywin32 / win32com` · `openpyxl` · `tkcalendar` ·
`customtkinter` · Somente Windows

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
