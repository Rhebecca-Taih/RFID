<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Agendamento%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Agendamento"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    Vigia uma pasta de rede onde vários arquivos de agendamento de<br>
    logística podem existir ao mesmo tempo e mantém sempre a versão<br>
    mais recente copiada para a pasta de envio, com nome fixo.
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

A cópia do arquivo de agendamento de logística para a pasta de envio era
feita manualmente, várias vezes ao dia. Este robô automatiza essa etapa,
identificando sempre a versão mais recente entre os arquivos disponíveis
na origem.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Detecção do arquivo mais recente | Identifica a versão mais atual pela data de modificação real, mesmo com vários arquivos na origem ao mesmo tempo |
| Cópia com nome fixo | Salva sempre com o mesmo nome no destino, pronta para o próximo processo consumir |
| Verificação de integridade | Confere se o tamanho da cópia corresponde ao original antes de considerar sucesso |
| Pausa noturna | Encerra às 20h e retoma automaticamente às 7h30 |
| Alta disponibilidade | Pode ser iniciado em qualquer máquina da rede, com proteção contra duas execuções simultâneas |

## ⋆˚✮ Destaques técnicos

- **Lock distribuído com heartbeat** — impede duas máquinas copiando ao
  mesmo tempo; se a máquina ativa parar de responder por mais de duas
  horas, outra assume o processamento automaticamente.
- **Chamadas de rede com limite de tempo** — toda operação que toca a
  pasta de rede (listar, copiar, ler data de modificação) executa com um
  teto de tempo próprio, para nunca ficar bloqueada indefinidamente numa
  conexão instável.
- **Recópia ao retomar da pausa noturna** — garante que a versão mais
  recente esteja disponível no destino, mesmo sem mudança detectada
  durante a pausa.
- **Checagem periódica e histórico arquivado** — a cada 3 horas, a origem
  é conferida contra o último arquivo copiado, e o histórico de cada dia
  fica arquivado por 30 dias.
- **Continuidade com a rede indisponível** — o ciclo principal é
  supervisionado e reiniciado após uma falha inesperada; enquanto a rede
  está inacessível, os registros seguem numa pasta local, e o log
  principal indica o período de indisponibilidade quando o acesso volta.
- **Auto-instalação** — dependências instaladas automaticamente na
  primeira execução, com progresso visível na tela.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
1. Lista os arquivos da origem e identifica o mais recente
   (por data de modificação real)
2. Confere se a origem mudou desde a última verificação
    ├─ Não mudou → aguarda a próxima verificação
    └─ Mudou     → aguarda um intervalo curto, copia, confere o tamanho e registra o resultado
3. Copia para o destino, sempre com nome fixo
4. Pausa automática à noite, retomada automática pela manhã
```

### ✮ Pré-Requisitos

Este robô depende da rede corporativa — não é executável fora desse
ambiente, nem para teste. Este repositório está publicado como peça de
portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Interpretador que executa o robô |
| Windows | Único sistema operacional suportado |
| Acesso à rede corporativa | Pastas de origem e destino do arquivo monitorado |

### ✮ Configuração

⋆˚✮ A configuração real fica em `Config_Cg/.env` (não versionado).
Referências em `Config_Cg/env.exemplo`.

| Variável | O que controla |
| :--- | :--- |
| `ORIGEM_PASTA` / `ORIGEM_PADRAO` | Pasta de origem e padrão de nome dos arquivos monitorados |
| `DESTINO_PASTA` / `NOME_DESTINO` | Pasta de destino e nome fixo salvo ali |
| `MINUTOS_ESPERA` | Minutos de espera após detectar um arquivo novo, antes de copiar |
| `INTERVALO_CHECK` | Segundos entre cada verificação |
| `MAX_TENTATIVAS` | Tentativas de cópia antes de registrar falha definitiva |

## ⋆˚✮ Stack

`Python 3.10+` · `customtkinter` · `pystray` · `python-dotenv` · Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
