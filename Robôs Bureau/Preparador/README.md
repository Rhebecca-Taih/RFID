<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:000000,100:8323b5&section=header&text=%E2%8B%86%CB%9A%CB%96%C2%B0Preparador%E2%8B%86%CB%9A%CB%96%C2%B0&fontSize=18&fontColor=deaaf9&fontAlignY=34" alt="Preparador"/>

<div align="center">
  <font size="4" color="#8323B5"><b>⋆.˚✮𖹭✮˚.⋆ VISÃO GERAL ⋆.˚✮𖹭✮˚.⋆</b></font>
</div>

<br>

<div align="center">
  <samp>
    A pessoa escolhe Data e Setor na tela; o robô atualiza a query de<br>
    pedidos, valida os fornecedores e entrega a fila pronta para o<br>
    Aprovador processar.
  </samp>
</div>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=deaaf9" alt="Python" />
  <img src="https://img.shields.io/badge/Excel_·_win32com-000000?style=for-the-badge&logo=microsoftexcel&logoColor=deaaf9" alt="Excel / win32com" />
  <img src="https://img.shields.io/badge/status-finalizado-8323B5?style=for-the-badge" alt="Status: finalizado" />
</div>

<br>

## ⋆˚✮ Contexto

Primeira etapa do pipeline de aprovação de pedidos: a partir de uma data e
um setor escolhidos manualmente, prepara a fila que o Aprovador vai
processar em seguida — sem precisar mexer em fórmula ou planilha
diretamente.

## ⋆˚✮ Funcionalidades

| Funcionalidade | Descrição |
| :--- | :--- |
| Atualização de query via Excel | Atualiza a query de pedidos (RefreshAll) por automação do Excel, sem intervenção manual |
| Validação de dados | Confere se a query trouxe os dados esperados antes de seguir |
| Validação de fornecedor | Pausa e mostra uma tela de revisão quando encontra um fornecedor ainda não mapeado |
| Entrega automática ao Aprovador | Copia o resultado pronto para a pasta vigiada pelo Aprovador |
| Acompanhamento do ciclo | Mostra o tempo decorrido enquanto aguarda o sinal de conclusão do Aprovador |

## ⋆˚✮ Destaques técnicos

- **Automação de Excel via win32com** — atualiza a query (RefreshAll) e
  confere se os dados trazidos correspondem ao esperado antes de seguir.
- **Validação de fornecedor protegida** — pausa e mostra uma tela de
  revisão quando encontra um fornecedor ainda não mapeado.
- **Espera não bloqueante pelo Aprovador** — mostra o tempo decorrido
  enquanto aguarda o sinal de conclusão, com opção de seguir sem esperar
  o sinal a qualquer momento.
- **Auto-instalação** — dependências instaladas automaticamente na
  primeira execução, com progresso visível na tela.

## ⋆˚✮ Aprofundamento do Projeto

### ✮ Como funciona

```text
Pessoa escolhe Data + Setor e clica em Processar
│
├─ Atualiza a query, valida os dados trazidos, ajusta a fórmula da
│   última coluna
├─ Copia o resultado para a pasta do Aprovador
│
└─ Aguarda o sinal do Aprovador
    ├─ Ciclo concluído  → libera a tela para a próxima data
    └─ Falha sinalizada → mostra o motivo, mesmas opções
```

### ✮ Pré-Requisitos

Este robô depende da rede corporativa — não é executável fora desse
ambiente, nem para teste. Este repositório está publicado como peça de
portfólio.

| Ferramenta | Motivo |
| :--- | :--- |
| Python 3.10+ | Interpretador que executa o robô |
| Windows + Excel | Automação via win32com exige Excel instalado |
| Acesso à rede corporativa | Planilha de fornecedores e entrega da fila para o Aprovador |

### ✮ Configuração

⋆˚✮ A configuração real fica em `../Config_Cg/.env` (não versionado).
Referências em `../Config_Cg/env.exemplo`.

| Variável | O que controla |
| :--- | :--- |
| `CAMINHO_FORNECEDORES` | Planilha de mapeamento de fornecedores conhecidos |
| `SETORES_PREPARADOR` | Setores disponíveis na tela, separados por vírgula |

## ⋆˚✮ Stack

`Python 3.10+` · `pywin32 / win32com` · `openpyxl` · `customtkinter` ·
`tkcalendar` · Somente Windows

## ⋆˚✮ Autora

Feito por [Rhebecca Tainara](https://linkedin.com/in/rhebecca-tainara)

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=0:8323b5,100:000000&section=footer" alt=""/>
