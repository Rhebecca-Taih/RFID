<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Controle%20KPI%20OneDrive%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Controle KPI OneDrive"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    Monitora um ou mais arquivos na rede e mantém cópias atualizadas em<br>
    pastas locais sincronizadas pelo OneDrive — para que os indicadores<br>
    subam automaticamente para o SharePoint, sem depender de ninguém<br>
    copiar o arquivo manualmente.
  </samp>
</div>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=deaaf9" alt="Python" />
  <img src="https://img.shields.io/badge/Windows-000000?style=for-the-badge&logo=windows11&logoColor=deaaf9" alt="Windows" />
  <img src="https://img.shields.io/badge/status-finalizado-8323B5?style=for-the-badge" alt="Status: finalizado" />
</div>

<br>

## ⋆˚✮ Contexto

Cada indicador do setor precisa de um arquivo sempre atualizado numa pasta
sincronizada pelo OneDrive, para o SharePoint refletir o dado mais
recente. Este robô processa quantas tarefas forem configuradas, cada uma
com sua própria origem e destino.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Multi-tarefa | Processa quantos arquivos forem configurados, sem precisar mexer no código para adicionar um novo |
| Cópia condicional | Só copia quando a origem realmente muda (data de modificação + tamanho) |
| Verificação de sincronização real | Confere o status de sincronização do OneDrive (o mesmo indicador do Explorer) após cada cópia |
| Sincronização manual | Botão "Sincronizar agora" na bandeja, além do ciclo automático |
| Usuário nunca fixo | O destino é resolvido a partir do usuário atual do Windows, funciona em qualquer perfil |

## ⋆˚✮ Destaques técnicos

- **Status real de sincronização** — lê o mesmo indicador que aparece no
  Explorer via COM do Shell do Windows, em vez de inferir por atributos
  de arquivo.
- **Multi-tarefa configurável** — cada tarefa é um trio de variáveis no
  `.env`; adicionar uma nova não exige mexer no código.
- **Usuário nunca fixo** — o destino é resolvido a partir do usuário
  atual do Windows em tempo real, funciona em qualquer perfil sem
  reconfiguração.
- **Lock distribuído com heartbeat** — impede duas máquinas copiando as
  mesmas tarefas ao mesmo tempo; se a máquina ativa parar de responder
  por mais de duas horas, outra assume o processamento.
- **Continuidade com a rede indisponível** — o ciclo principal é
  supervisionado e reiniciado após uma falha inesperada; enquanto a rede
  está inacessível, os registros seguem numa pasta local, e o log
  principal indica o período de indisponibilidade quando o acesso volta.
- **Auto-instalação** — dependências instaladas automaticamente na
  primeira execução, com progresso visível na tela.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Inicia uma verificação por tarefa, em intervalo fixo
│
├─ Compara data de modificação + tamanho da origem com o último conhecido
│   ├─ Igual      → nada mudou, aguarda a próxima checagem
│   └─ Diferente  → aguarda um intervalo curto e copia
│       ├─ Confere se o tamanho da cópia corresponde ao original
│       └─ Confere o status real de sincronização do OneDrive
│
└─ "Sincronizar agora" na bandeja força a checagem de todas as tarefas
```

### ✮ Pré-Requisitos

⋆˚✮ Antes de começar, você vai precisar ter instalado em sua máquina:

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Interpretador que executa o robô |
| Windows | Único sistema operacional suportado (usa COM do Shell) |

### ✮ Configuração

Copie `Config_Cg/env.exemplo`, renomeie para `.env` (mantendo dentro da
pasta `Config_Cg`) e preencha com os dados reais.

| Variável | O que controla |
| :--- | :--- |
| `PASTA_ONEDRIVE_BASE` | Nome da pasta raiz do OneDrive dentro do perfil do usuário |
| `TAREFA_N_ORIGEM` / `TAREFA_N_DESTINO_SUBPASTA` / `TAREFA_N_NOME` | Cada tarefa (N = 1, 2, 3...), origem e destino |
| `TAREFA_N_LINK_SHAREPOINT` | Link da biblioteca, mostrado na tela se o destino ainda não existir nesse PC |
| `INTERVALO_CHECK_SEGUNDOS` | Segundos entre cada verificação |
| `SEGUNDOS_ESPERA` | Espera após detectar mudança, antes de copiar |
| `MAX_TENTATIVAS` | Tentativas de cópia antes de registrar falha definitiva |

## ⋆˚✮ Stack

`Python 3.10+` · `customtkinter` · `pystray` · `python-dotenv` · Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
