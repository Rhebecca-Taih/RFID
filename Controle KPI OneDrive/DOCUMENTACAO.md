<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Controle%20KPI%20OneDrive%20%E2%80%94%20Documenta%C3%A7%C3%A3o%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Controle KPI OneDrive — Documentação"/>

Manual de referência do robô Controle KPI OneDrive: como operar no dia a
dia e como o sistema é construído por dentro. Complementa o
[README](./README.md), que apresenta o projeto em linhas gerais.

---

## ⋆˚✮ Guia de Uso

### ✮ Antes de iniciar

⋆˚✮ O ambiente precisa ter:

| Item | Por quê |
| :--- | :--- |
| Python instalado nesta máquina | O arquivo do robô (`.pyw`) é executado pelo Python — sem ele instalado, o duplo clique não abre nada |
| Arquivo `.env` configurado | Define cada tarefa (origem, destino, nome) — sem ele o robô não tem o que vigiar |
| OneDrive instalado, aberto e logado nesta máquina | Sem o OneDrive em execução e logado, o arquivo é copiado localmente mas não sobe para a nuvem |
| Pastas de destino já sincronizadas pelo OneDrive | A tela de verificação mostra um link direto para a biblioteca do SharePoint quando a pasta ainda não existe localmente |

### ✮ Como iniciar

1. Acesse a pasta do robô: `Controle KPI OneDrive/`.
2. Dê duplo clique no arquivo `Controle_KPI_OneDrive_auto.pyw`.
3. A janela de lançamento abre automaticamente e percorre pelas telas descritas
   abaixo, na ordem.
4. Na última tela, clique em **Iniciar**.
5. A janela fecha e o robô segue em execução pela bandeja do sistema (ícone
   próximo ao relógio, no canto da tela).

### ✮ Tela a tela

**Tela 1 — Bibliotecas**
Confere se as bibliotecas necessárias já estão instaladas nesta máquina e
instala automaticamente o que faltar. Avança automaticamente ao concluir.

**Tela 2 — Tarefas**
Mostra cada tarefa configurada no `.env`, com o status de acesso à
origem e ao destino, além do status do OneDrive (em execução e com conta
logada). Se alguma pasta de destino não existir ainda nesta máquina,
aparece um link direto para a biblioteca correspondente no SharePoint. Se
algo estiver pendente, o botão fica como **Verificar novamente** até
tudo ser corrigido.

**Tela 3 — Final**
Confirma que tudo está certo e libera o botão **Iniciar**.

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
| Sincronizar agora | Força a checagem de todas as tarefas imediatamente, sem esperar o próximo ciclo |
| Parar robô | Encerra o processo e libera o controle de instância única |

**Janela de histórico ao vivo**
Mostra os blocos de log do dia, coloridos por tipo (sucesso, aviso,
erro), atualizada automaticamente conforme o robô registra eventos novos.

O robô vigia cada tarefa continuamente, comparando a data de modificação
e o tamanho da origem com o último valor conhecido. Ao detectar uma
mudança, espera um curto intervalo antes de copiar — tempo suficiente
para quem está salvando o arquivo terminar.

### ✮ Como encerrar

Clique com o botão direito no ícone da bandeja e selecione **Parar robô**.

### ✮ Mensagens do histórico e o que fazem

Este robô não grava status por item — ele registra o resultado de cada
cópia no histórico. As mensagens mais relevantes:

| Mensagem | O que significa | O que fazer |
| :--- | :--- | :--- |
| Copiado com sucesso | Arquivo copiado e com o tamanho conferido | Nenhuma |
| Cópia incompleta | O tamanho copiado diverge do original | O robô tenta de novo automaticamente; se persistir, conferir a rede |
| Arquivo permaneceu em uso | O arquivo de destino estava aberto em outro programa durante todas as tentativas | Fechar o arquivo na máquina que estiver com ele aberto |
| OneDrive não está em execução | O arquivo foi copiado localmente, mas não vai subir para a nuvem enquanto o OneDrive não for reaberto | O robô tenta reabrir automaticamente; se não conseguir, abrir manualmente |
| Nenhuma conta vinculada ao OneDrive | O arquivo foi copiado localmente, mas não sobe para a nuvem até alguém logar | Fazer login no OneDrive manualmente (exige verificação adicional, não dá para automatizar) |
| Arquivo(s) parecido(s) na pasta de destino — possível conflito de sincronização | O OneDrive pode ter criado uma cópia de conflito (geralmente com o nome do computador ao lado) | Verificar manualmente qual versão é a correta na pasta de destino |
| Rede indisponível de [início] até [fim] | A pasta de log na rede ficou inacessível nesse período | Nenhuma — os registros do período ficam na pasta local indicada na própria mensagem |
| O loop principal parou por um erro inesperado -- reiniciando | Uma falha inesperada interrompeu o ciclo, que foi reiniciado em seguida | Nenhuma, se não se repetir; se se repetir, consultar `logs/historico_erros.txt` |

⋆˚✮ O histórico de erros técnicos completo fica em
`logs/historico_erros.txt`, com data e hora de cada ocorrência.

---

## ⋆˚✮ Documentação Técnica

### ✮ Arquitetura

```text
Pasta de rede (arquivo de origem de cada tarefa)
   │  mudança de data de modificação ou tamanho
   ▼
Robô Controle KPI OneDrive
   ├─ Copia para a pasta local sincronizada pelo OneDrive
   └─ Confere se o OneDrive está em execução, logado, e se não há conflito
          │
          ▼
   OneDrive sincroniza para o SharePoint
```

Robô independente, sem relação de entrada/saída com os outros robôs do
repositório — processa quantas tarefas forem configuradas no `.env`,
cada uma com sua própria origem e destino.

### ✮ Módulos

#### ⋆ Controle de instância única

Antes de abrir a janela de lançamento, o robô grava um arquivo de lock
com PID, nome da máquina, data de início e um heartbeat atualizado a
cada 10 minutos. Na mesma máquina, a verificação confere se o processo
do lock ainda está em execução; em outra máquina, o lock só é liberado
depois de 2 horas sem atualização — evita duas máquinas copiando as
mesmas tarefas ao mesmo tempo.

#### ⋆ Múltiplas tarefas configuráveis

Cada tarefa é lida do `.env` como um conjunto numerado de variáveis
(origem, subpasta de destino, nome, link do SharePoint) — adicionar uma
nova tarefa não exige alterar o código.

#### ⋆ Cópia condicional com nova tentativa

Compara data de modificação e tamanho da origem com o último valor
conhecido antes de copiar, evitando cópias desnecessárias. Confere o
tamanho do arquivo copiado contra o original e tenta de novo em caso de
divergência ou arquivo em uso.

#### ⋆ Diagnóstico pós-cópia do OneDrive

Depois de cada cópia bem-sucedida, confere se o processo do OneDrive
está em execução, se existe uma conta vinculada (via registro do
Windows) e se há arquivos com nome parecido na pasta de destino (sinal
de conflito de sincronização) — sem essas três condições, o arquivo pode
estar copiado localmente sem nunca chegar à nuvem.

#### ⋆ Histórico ao vivo

Lê o arquivo de log e separa em blocos, classificando cada um por tipo
(sucesso, aviso, erro) pela presença de símbolos e palavras específicas,
exibindo com cor própria na janela de histórico.

#### ⋆ Loop principal com sincronização manual

Alterna entre vigiar todas as tarefas e aguardar o próximo intervalo
configurado, mas pode ser interrompido a qualquer momento pelo botão
"Sincronizar agora" da bandeja, que força uma checagem imediata.

#### ⋆ Continuidade com a rede indisponível

O loop principal executa sob supervisão: uma falha inesperada é
registrada e o loop é reiniciado após 30 segundos, sem encerrar o
processo. Quando a pasta de log na rede está inacessível, os registros
vão para uma pasta local da máquina
(`%LOCALAPPDATA%\RobosBureau\Controle KPI OneDrive\`, mantida por 30
dias); ao restabelecer o acesso, o log da rede recebe uma linha com o
período de indisponibilidade e a localização dos registros locais.

### ✮ Decisões de Arquitetura

- **O destino é resolvido a partir do usuário atual do Windows, não de
  um caminho fixo** — a pasta do OneDrive fica dentro do perfil de cada
  usuário; resolver dinamicamente evita reconfiguração ao trocar de
  máquina ou de conta.
- **Confere o status do OneDrive depois de copiar, não só a cópia em
  si** — um arquivo copiado com sucesso localmente pode nunca chegar à
  nuvem se o OneDrive estiver fechado ou deslogado; sem essa conferência,
  essa falha passaria despercebida.
- **Não tenta automatizar o login do OneDrive** — a autenticação exige
  verificação adicional (MFA), que só uma pessoa pode completar; o robô
  detecta a ausência de conta logada e avisa, em vez de tentar contornar.
- **O lock considera o nome da máquina antes de verificar o processo** —
  a lista de processos só enxerga a própria máquina; para uma instância
  em outra máquina, o critério é o tempo desde o último heartbeat.
- **Registros alternam para uma pasta local quando a rede está
  indisponível** — o log fica na rede; o registro local preserva a
  sequência de eventos do período sem acesso e o processamento continua
  até o acesso voltar.
- **Primeira sincronização ao iniciar é incondicional, mesmo sem detectar
  mudança** — garante que o destino comece atualizado mesmo que o robô
  tenha ficado desligado por um tempo e a origem tenha mudado nesse
  intervalo.

### ✮ Configuração

⋆˚✮ Variáveis de ambiente usadas por este robô:

| Variável | O que controla |
| :--- | :--- |
| `PASTA_ONEDRIVE_BASE` | Nome da pasta raiz do OneDrive dentro do perfil do usuário |
| `TAREFA_N_ORIGEM` / `TAREFA_N_DESTINO_SUBPASTA` / `TAREFA_N_NOME` | Cada tarefa (N = 1, 2, 3...), origem e destino |
| `TAREFA_N_LINK_SHAREPOINT` | Link da biblioteca, mostrado na tela se o destino ainda não existir nesse PC |
| `INTERVALO_CHECK_SEGUNDOS` | Segundos entre cada verificação |
| `SEGUNDOS_ESPERA` | Espera após detectar mudança, antes de copiar |
| `MAX_TENTATIVAS` | Tentativas de cópia antes de registrar falha definitiva |
| `NOME_CRIADOR` / `LINK_GITHUB_CRIADOR` | Crédito de autoria exibido no cabeçalho da janela |

### ✮ Stack

`Python 3.10+` · `customtkinter` · `pystray` · `python-dotenv` ·
Somente Windows

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
