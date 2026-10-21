<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Agendamento%20%E2%80%94%20Documenta%C3%A7%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Agendamento — Documentação"/>

Manual de referência do robô de Agendamento: como operar no dia a dia e
como o sistema é construído por dentro. Complementa o
[README](./README.md), que apresenta o projeto em linhas gerais.

---

## ⋆˚✮ Guia de Uso

### ✮ Antes de iniciar

⋆˚✮ O ambiente precisa ter:

| Item | Por quê |
| :--- | :--- |
| Python instalado nesta máquina | O arquivo do robô (`.pyw`) é executado pelo Python — sem ele instalado, o duplo clique não abre nada |
| Arquivo `.env` configurado | Define as pastas de origem e destino — sem ele o robô não sabe o que monitorar |
| Acesso às pastas de origem e destino na rede | É o que o robô vigia e para onde copia — sem acesso, ele mostra aviso mas continua tentando automaticamente |

### ✮ Como iniciar

1. Acesse a pasta do robô: `Automação Agendamento/`.
2. Dê duplo clique no arquivo `Agendamento_auto.pyw`.
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

**Tela 2 — Pastas**
Confirma se a pasta de origem e a pasta de destino estão acessíveis
agora. Se alguma não estiver, mostra aviso mas permite continuar — o
robô tenta de novo automaticamente depois de iniciar.

**Tela 3 — Final**
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
| Ver histórico | Abre uma janela com o histórico do dia, atualizada ao vivo |
| Status | Mostra o estado atual sem abrir nada (apenas informativo) |
| Parar robô | Encerra o processo e libera o controle de instância única |

**Janela de histórico ao vivo**
Mostra os blocos de log do dia, coloridos por tipo (sucesso, aviso,
erro), atualizada automaticamente conforme o robô registra eventos novos. O
botão "Abrir arquivo bruto" abre o `.txt` original no bloco de notas.

O robô vigia a pasta de origem continuamente. Ao detectar um arquivo mais
novo, espera alguns minutos (configurável) antes de copiar — tempo
suficiente para quem está editando terminar e salvar. Das 20h às 7h30, o
robô entra em pausa noturna e retoma automaticamente, sem precisar de ação
manual. Ao retomar, copia de novo o arquivo mais recente, mantendo o
destino atualizado mesmo que a pasta tenha sido limpa durante a noite.

A cada 3 horas, independentemente de haver mudança na origem, o
histórico recebe uma checagem com o arquivo mais recente da origem e a
indicação de que ele corresponde, ou não, ao último arquivo copiado.

### ✮ Como encerrar

Clique com o botão direito no ícone da bandeja e selecione **Parar robô**.
Fechar a janela do terminal sem usar essa opção pode deixar o controle de
instância única travado até a próxima verificação automática.

### ✮ Mensagens do histórico e o que fazem

Este robô não grava status por item — ele só copia um arquivo por vez. A
tabela abaixo cobre os eventos que aparecem no histórico:

| Mensagem | O que significa | O que fazer |
| :--- | :--- | :--- |
| Copiado com sucesso | Arquivo novo copiado e com o tamanho conferido | Nenhuma |
| Cópia incompleta | O tamanho copiado diverge do original | O robô tenta de novo automaticamente; se persistir após todas as tentativas, conferir a rede |
| Arquivo permaneceu em uso | O destino estava aberto em outro programa (ex.: Excel) durante todas as tentativas | Fechar o arquivo na máquina que estiver com ele aberto |
| Erro/timeout na cópia | Falha inesperada ou rede sem responder durante a cópia | O robô tenta de novo automaticamente; se persistir, conferir a conexão de rede |
| Nenhum arquivo encontrado na pasta de origem | Não há nenhum arquivo no padrão esperado na pasta de origem | Confirmar se o arquivo existe e segue o padrão de nome esperado |
| A pasta de rede não respondeu | A pasta de origem ou destino não respondeu dentro do tempo esperado | Nenhuma — o robô tenta de novo automaticamente no próximo ciclo |
| Checagem periódica — corresponde ao já processado? SIM | O arquivo mais recente da origem é o mesmo já copiado | Nenhuma |
| Checagem periódica — corresponde ao já processado? NÃO | Existe na origem um arquivo mais recente que ainda não foi copiado | Conferir o histórico das últimas horas; a divergência também fica registrada em `logs/historico_erros.txt` |
| Rede indisponível de [início] até [fim] | A pasta de log na rede ficou inacessível nesse período | Nenhuma — os registros do período ficam na pasta local indicada na própria mensagem |
| O loop principal parou por um erro inesperado -- reiniciando | Uma falha inesperada interrompeu o ciclo, que foi reiniciado em seguida | Nenhuma, se não se repetir; se se repetir, consultar `logs/historico_erros.txt` |

⋆˚✮ O histórico de erros técnicos completo fica em
`logs/historico_erros.txt`, com data e hora de cada ocorrência — use esse
arquivo para investigar um problema que se repete. O histórico de cada dia
anterior fica em `logs/historico_arquivado/`, por 30 dias.

---

## ⋆˚✮ Documentação Técnica

### ✮ Arquitetura

Robô independente, sem relação de entrada/saída com os outros robôs do
repositório:

```text
Pasta de origem (rede)
   │  arquivo mais recente que corresponde ao padrão configurado
   ▼
Robô Agendamento
   │  copia com nome fixo, após confirmar tamanho
   ▼
Pasta de destino (rede)
```

### ✮ Módulos

#### ⋆ Controle de instância única

Antes de abrir a janela de lançamento, o robô grava um arquivo de lock
com PID, nome da máquina e um heartbeat atualizado a cada 10 minutos.
Outra máquina só é liberada para iniciar se o lock atual estiver há mais
de 2 horas sem atualização — evita duas máquinas monitorando e copiando
ao mesmo tempo.

#### ⋆ Resolução da origem

Localiza todos os arquivos que correspondem ao padrão configurado na pasta
de origem e escolhe o de modificação mais recente. Mais de um arquivo ao
mesmo tempo é esperado, não é tratado como problema.

#### ⋆ Operações com tempo limite

Toda operação de arquivo na rede (checar existência, data de
modificação, tamanho, copiar) é executada com um tempo limite próprio, numa
thread separada — uma pasta de rede que trava não responde com erro, só
fica sem responder, e sem esse limite o robô ficaria preso
indefinidamente esperando.

#### ⋆ Cópia com nova tentativa

Copia com nome fixo e confere o tamanho do arquivo copiado contra o
original antes de considerar sucesso. Se o destino estiver em uso
(arquivo aberto em outro programa), espera mais tempo antes de tentar de
novo do que em outros tipos de erro.

#### ⋆ Histórico ao vivo

Lê o arquivo de log e separa em blocos, classificando cada um por tipo
(sucesso, aviso, erro) pela presença de palavras e símbolos específicos,
exibindo com cor própria na janela de histórico.

#### ⋆ Loop principal

Alterna entre vigiar a origem e respeitar a pausa noturna, atualizando o
heartbeat do lock em intervalos regulares mesmo durante a pausa. Ao sair
da pausa, copia novamente o arquivo mais recente da origem.

#### ⋆ Checagem periódica

A cada 3 horas, independentemente do gatilho por data de modificação,
compara o arquivo mais recente da origem com o último arquivo copiado e
registra o resultado no histórico. Uma divergência também é registrada
no histórico de erros.

#### ⋆ Histórico diário arquivado

Na virada do dia, o log do dia anterior é movido para
`logs/historico_arquivado/`, com a data do próprio log no nome do
arquivo, e mantido por 30 dias.

#### ⋆ Continuidade com a rede indisponível

O loop principal executa sob supervisão: uma falha inesperada é
registrada e o loop é reiniciado após 30 segundos, sem encerrar o
processo. Quando a pasta de log na rede está inacessível, os registros
vão para uma pasta local da máquina (`%LOCALAPPDATA%\RobosBureau\Agendamento\`,
mantida por 30 dias); ao restabelecer o acesso, o log da rede recebe uma
linha com o período de indisponibilidade e a localização dos registros
locais.

### ✮ Decisões de Arquitetura

- **Escolhe o arquivo mais recente entre vários na origem, não o único
  esperado** — mais de uma cópia na pasta de origem ao mesmo tempo é
  normal (ex.: versões antigas não removidas), e tratar isso como erro
  pararia o robô sem necessidade.
- **Só atualiza a data de modificação conhecida depois de confirmar
  cópia bem-sucedida** — evita que uma tentativa falha seja considerada
  "já vista", o que faria o robô ignorar aquele arquivo até a próxima
  alteração real.
- **Confere o tamanho do arquivo depois de copiar, não só a existência**
  — uma cópia pode terminar sem erro e ainda assim estar incompleta
  (rede caindo no meio); conferir o tamanho detecta esse caso.
- **Espera mais tempo quando o erro é "arquivo em uso" do que em outros
  erros** — esse caso específico normalmente se resolve assim
  que alguém fecha o arquivo, então vale a pena esperar mais antes de
  desistir da tentativa.
- **Cada operação de arquivo é executada com tempo limite numa thread separada**
  — uma pasta de rede indisponível trava a chamada sem gerar exceção;
  sem o tempo limite, o robô ficaria parado esperando para sempre.
- **Checagem periódica independente do gatilho de mudança** — a origem
  pode passar um dia inteiro sem alteração, então a ausência de mudança
  não indica problema; a checagem a cada 3 horas deixa registro
  verificável de que a origem foi consultada.
- **Arquiva o histórico diário em vez de substituí-lo** — mantém o
  registro dos dias anteriores disponível para consulta posterior.
- **Registros alternam para uma pasta local quando a rede está
  indisponível** — o log fica na rede; o registro local preserva a
  sequência de eventos do período sem acesso e o processamento continua
  até o acesso voltar.

### ✮ Configuração

⋆˚✮ Variáveis de ambiente usadas por este robô:

| Variável | O que controla |
| :--- | :--- |
| `ORIGEM_PASTA` | Pasta de rede monitorada |
| `ORIGEM_PADRAO` | Padrão de nome dos arquivos de origem (aceita curinga) |
| `DESTINO_PASTA` | Pasta de rede de destino |
| `NOME_DESTINO` | Nome fixo salvo no destino, independente do nome original |
| `MINUTOS_ESPERA` | Tempo de espera após detectar alteração, antes de copiar |
| `INTERVALO_CHECK` | Intervalo entre verificações da pasta de origem |
| `MAX_TENTATIVAS` | Tentativas de cópia antes de desistir no ciclo |
| `NOME_CRIADOR` / `LINK_GITHUB_CRIADOR` | Crédito de autoria exibido no cabeçalho da janela |

### ✮ Stack

`Python 3.10+` · `customtkinter` · `pystray` · Somente Windows

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
