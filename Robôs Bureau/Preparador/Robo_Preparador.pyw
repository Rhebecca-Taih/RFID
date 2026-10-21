# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# BIBLIOTECAS
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
import os
import sys
import time
import shutil
import stat
import subprocess
import threading
import importlib
import webbrowser
from datetime import datetime

import tkinter as tk

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# DETECÇÃO PARA AUTO-INSTALAÇÃO DE BIBLIOTECAS
# Instalação ao vivo em _checar_ambiente (tela Bibliotecas).
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_LIBS = [
    ("openpyxl",      "openpyxl"),
    ("win32com",      "pywin32"),
    ("dotenv",        "python-dotenv"),
    ("tkcalendar",    "tkcalendar"),
    ("customtkinter", "customtkinter"),
]
_STATUS_INSTALL = {}
for _ni, _np in _LIBS:
    try:
        __import__(_ni)
        _STATUS_INSTALL[_np] = "ok"
    except ImportError:
        _STATUS_INSTALL[_np] = "faltando"


if _STATUS_INSTALL.get("customtkinter") == "faltando":
    _splash = tk.Tk()
    _splash.title("Robô Preparador")
    _splash.configure(bg="#18181B")
    _splash.resizable(False, False)
    _sw, _sh = _splash.winfo_screenwidth(), _splash.winfo_screenheight()
    _splash.geometry(f"360x110+{(_sw-360)//2}+{(_sh-110)//2}")
    tk.Label(_splash, text="Preparando o ambiente pela primeira vez...",
             font=("Segoe UI", 11), fg="#F2F2F2", bg="#18181B").pack(pady=(28, 6))
    tk.Label(_splash, text="Instalando customtkinter...",
             font=("Segoe UI", 9), fg="#A8A8A8", bg="#18181B").pack()
    _splash.update()
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "customtkinter", "--quiet"],
                       capture_output=True, timeout=180, creationflags=_NO_WINDOW)
        __import__("customtkinter")
        _STATUS_INSTALL["customtkinter"] = "ok"
    except Exception:
        _STATUS_INSTALL["customtkinter"] = "faltando"
    _splash.destroy()

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# IMPORTS EXTERNOS
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_IMPORTS_OK = True
_IMPORTS_ERRO = ""

def _corrigir_dll_pywin32():
    try:
        import site
        pastas = list(site.getsitepackages())
        try:
            pastas.append(site.getusersitepackages())
        except Exception:
            pass
        for base in pastas:
            if os.path.isdir(base):
                site.addsitedir(base)
            pasta_dll = os.path.join(base, "pywin32_system32")
            if os.path.isdir(pasta_dll):
                try:
                    os.add_dll_directory(pasta_dll)
                except Exception:
                    pass
    except Exception:
        pass

def _tentar_importar_reais():
    global _IMPORTS_OK, _IMPORTS_ERRO
    global ctk, pythoncom, win32, load_dotenv, Calendar
    try:
        import customtkinter as ctk
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    except Exception as _ex:
        _IMPORTS_OK = False
        _IMPORTS_ERRO = f"customtkinter -- {_ex}"
        return

    _corrigir_dll_pywin32()
    try:
        import pythoncom
        import win32com.client as win32
        from dotenv import load_dotenv
        from tkcalendar import Calendar
        _IMPORTS_OK = True
        _IMPORTS_ERRO = ""
    except Exception as _ex:
        _IMPORTS_OK = False
        _IMPORTS_ERRO = str(_ex)

_tentar_importar_reais()


pasta_script = os.path.dirname(os.path.abspath(__file__))
pasta_raiz   = os.path.dirname(pasta_script)

CAMINHO_ENV = os.path.join(pasta_raiz, "Config_Cg", ".env")

def _carregar_env():
    try:
        from dotenv import load_dotenv as _load_dotenv
        _load_dotenv(dotenv_path=CAMINHO_ENV)
        return
    except ImportError:
        pass
    try:
        with open(CAMINHO_ENV, "r", encoding="utf-8-sig") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                chave, valor = linha.split("=", 1)
                valor = valor.strip()
                if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                    valor = valor[1:-1]
                os.environ.setdefault(chave.strip(), valor)
    except Exception:
        pass

_carregar_env()

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# CONFIGURAÇÕES
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
ARQUIVO_QUERY     = os.path.join(pasta_script, "Query_Aprovar", "Aprovar_Query.xlsx")
PASTA_APROVADOR   = os.path.join(pasta_raiz, "Aprovador")
CAMINHO_FILA      = os.path.join(PASTA_APROVADOR, "Fila_Aprovacao", "Fila_Aprovacao.xlsx")


CAMINHO_STATUS_APROVADOR = os.path.join(PASTA_APROVADOR, "Fila_Aprovacao", "status_aprovador.txt")


ABA_CONFIGURACOES = "CONFIGURAÇÕES"
CELULA_DATA_ALVO  = "A2"
CELULA_SETOR_ALVO = "B2"
ABA_APROVACAO     = "APROVAÇÃO"


SETORES_DISPONIVEIS = [
    s.strip() for s in
    os.getenv("SETORES_PREPARADOR", "ELETRO-ELETRONICOS,BELEZA").split(",")
    if s.strip()
]


CAMINHO_FORNECEDORES = os.getenv("CAMINHO_FORNECEDORES", "")


HEARTBEAT_INTERVALO = 60
EXPIRACAO_LOCK       = 30 * 60


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# PALETA VISUAL
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
COR_FUNDO        = "#18181B"
COR_CARD         = "#242428"
COR_HEADER       = "#FFC72C"
COR_HEADER_TXT   = "#1A1A1A"
COR_TEXTO        = "#F2F2F2"
COR_DETALHE      = "#A8A8A8"
COR_MUTED        = "#7A7A7A"
COR_BORDA        = "#3A3A3C"
COR_CHIP_ATIVO   = "#FFC72C"
COR_CHIP_INATIVO = "#333336"
COR_BTN_C        = "#333336"
COR_BTN_C_TXT    = "#F2F2F2"
COR_OK           = "#4ADE80"
COR_OK_FUNDO     = "#173321"
COR_AVISO        = "#FBBF24"
COR_AVISO_FUNDO  = "#3A2E0C"
COR_ERRO         = "#F87171"
COR_ERRO_FUNDO   = "#3A1414"


NOME_CRIADOR      = os.getenv("NOME_CRIADOR",      "Rhebecca-Taih")
LINK_GITHUB_CRIADOR = os.getenv("LINK_GITHUB_CRIADOR", "https://github.com/Rhebecca-Taih")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# ARQUIVOS DE CONTROLE
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_pasta_logs    = os.path.join(pasta_script, "logs")
_pasta_runtime = os.path.join(pasta_script, "runtime")
try:
    os.makedirs(_pasta_logs,    exist_ok=True)
    os.makedirs(_pasta_runtime, exist_ok=True)
except Exception:
    pass

LOG_ARQUIVO          = os.path.join(_pasta_logs, "historico_preparador.txt")
LOG_ERROS_PERMANENTE = os.path.join(_pasta_logs, "historico_erros.txt")
LOCK_ARQUIVO         = os.path.join(_pasta_runtime, "preparador.lock")


_ui_log_callback = None

def _definir_callback_log(func):
    global _ui_log_callback
    _ui_log_callback = func

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOG
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _data_hoje():
    return datetime.now().strftime("%d/%m/%Y")

def _agora_completo():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def _gerenciar_log():
    sep = "=" * 60
    hoje = _data_hoje()
    if os.path.exists(LOG_ARQUIVO):
        try:
            with open(LOG_ARQUIVO, "r", encoding="utf-8") as f:
                f.readline()
                segunda = f.readline()
            if hoje not in segunda:
                os.remove(LOG_ARQUIVO)
        except Exception:
            try:
                os.remove(LOG_ARQUIVO)
            except Exception:
                pass
    if not os.path.exists(LOG_ARQUIVO):
        try:
            with open(LOG_ARQUIVO, "w", encoding="utf-8") as f:
                f.write(f"{sep}\n  LOG DE AUTOMACAO -- {hoje}\n{sep}\n\n")
        except Exception:
            pass

PASTA_LOG_LOCAL = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "RobosBureau", "Preparador")
DIAS_MANTER_LOG_LOCAL = 30
_rede_indisponivel_desde = None

def _limpar_logs_locais_antigos():
    try:
        limite = time.time() - DIAS_MANTER_LOG_LOCAL * 86400
        for nome in os.listdir(PASTA_LOG_LOCAL):
            caminho = os.path.join(PASTA_LOG_LOCAL, nome)
            if os.path.isfile(caminho) and os.path.getmtime(caminho) < limite:
                os.remove(caminho)
    except Exception:
        pass

def _registrar_log_local(texto):
    global _rede_indisponivel_desde
    if _rede_indisponivel_desde is None:
        _rede_indisponivel_desde = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        os.makedirs(PASTA_LOG_LOCAL, exist_ok=True)
        caminho = os.path.join(PASTA_LOG_LOCAL, f"log_{datetime.now().strftime('%d-%m-%Y')}.txt")
        arquivo_novo = not os.path.exists(caminho)
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(texto)
        if arquivo_novo:
            _limpar_logs_locais_antigos()
    except Exception:
        pass

def _aviso_rede_restabelecida():
    if _rede_indisponivel_desde is None:
        return ""
    return (f"⚠️  Rede indisponível de {_rede_indisponivel_desde} até "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}. Registros desse período em: {PASTA_LOG_LOCAL}")

def _confirmar_rede_ok():
    global _rede_indisponivel_desde
    _rede_indisponivel_desde = None

def registrar_log(mensagem, tag="normal"):
    hora = datetime.now().strftime("%H:%M:%S")
    linha = f"{mensagem}  [{hora}]"
    try:
        with open(LOG_ARQUIVO, "a", encoding="utf-8") as f:
            aviso = _aviso_rede_restabelecida()
            if aviso:
                f.write(f"{aviso}  [{hora}]\n")
            f.write(linha + "\n")
        _confirmar_rede_ok()
    except Exception:
        _registrar_log_local(f"[{_agora_completo()}] {mensagem}\n")
    if _ui_log_callback:
        try:
            _ui_log_callback(mensagem, hora, tag)
        except Exception:
            pass

def registrar_erro_permanente(msg):
    try:
        with open(LOG_ERROS_PERMANENTE, "a", encoding="utf-8") as f:
            f.write(f"[{_agora_completo()}] {msg}\n")
    except Exception:
        _registrar_log_local(f"[{_agora_completo()}] ERRO: {msg}\n")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOCK
# Formato do arquivo: PID|NOME_PC|DATA_INICIO|ULTIMO_HEARTBEAT|DATA_PEDIDO|SETOR
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _tentar_obter_lock(data_texto, setor):
    nome_pc = os.environ.get("COMPUTERNAME", "DESCONHECIDO")
    if os.path.exists(LOCK_ARQUIVO):
        try:
            with open(LOCK_ARQUIVO, "r") as f:
                partes = f.read().strip().split("|")
            pid_antigo   = int(partes[0])
            pc_antigo    = partes[1] if len(partes) > 1 else "?"
            dt_inicio    = partes[2] if len(partes) > 2 else "?"
            dt_heartbeat = partes[3] if len(partes) > 3 else dt_inicio
            data_antiga  = partes[4] if len(partes) > 4 else "?"
            setor_antigo = partes[5] if len(partes) > 5 else "?"

            if pc_antigo == nome_pc:
                r = subprocess.run(f'tasklist /FI "PID eq {pid_antigo}" /NH',
                                   shell=True, capture_output=True, text=True,
                                   creationflags=_NO_WINDOW)
                if str(pid_antigo) in r.stdout:
                    return False, {
                        "pc": pc_antigo, "inicio": dt_inicio,
                        "data": data_antiga, "setor": setor_antigo,
                    }

            else:
                try:
                    hb_dt = datetime.strptime(dt_heartbeat, "%d/%m/%Y %H:%M")
                    idade_seg = (datetime.now() - hb_dt).total_seconds()
                except Exception:
                    idade_seg = EXPIRACAO_LOCK
                if idade_seg < EXPIRACAO_LOCK:
                    return False, {
                        "pc": pc_antigo, "inicio": dt_inicio,
                        "data": data_antiga, "setor": setor_antigo,
                    }

        except Exception:
            pass

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    try:
        with open(LOCK_ARQUIVO, "w") as f:
            f.write(f"{os.getpid()}|{nome_pc}|{agora}|{agora}|{data_texto}|{setor}")
    except Exception:
        pass
    return True, None

def _atualizar_heartbeat_lock():
    try:
        if not os.path.exists(LOCK_ARQUIVO):
            return
        with open(LOCK_ARQUIVO, "r") as f:
            partes = f.read().strip().split("|")
        if not partes or int(partes[0]) != os.getpid():
            return
        partes[3] = datetime.now().strftime("%d/%m/%Y %H:%M")
        while len(partes) < 6:
            partes.append("?")
        with open(LOCK_ARQUIVO, "w") as f:
            f.write("|".join(partes))
    except Exception:
        pass

def _liberar_lock():
    try:
        if os.path.exists(LOCK_ARQUIVO):
            with open(LOCK_ARQUIVO, "r") as f:
                pid = int(f.read().strip().split("|")[0])
            if pid == os.getpid():
                os.remove(LOCK_ARQUIVO)
    except Exception:
        pass


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# QUERY E FILA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# Operações de rede podem deixar o arquivo somente leitura > o Excel precisa abrir para escrita.
def destravar_arquivo(caminho_arquivo):
    try:
        atributos_atuais = os.stat(caminho_arquivo).st_mode
        os.chmod(caminho_arquivo, atributos_atuais | stat.S_IWRITE)
        return True
    except Exception:
        return False

# Coluna localizada pelo nome > planilha reordenada continua funcionando.
def _achar_coluna_cabecalho(ws, nome_procurado, linha_cabecalho=1, max_col=60):
    alvo = nome_procurado.strip().upper()
    for c in range(1, max_col + 1):
        val = ws.Cells(linha_cabecalho, c).Value
        if val and str(val).strip().upper() == alvo:
            return c
    return None

def atualizar_query(data_texto, setor):
    excel = None
    wb = None
    try:
        destravar_arquivo(ARQUIVO_QUERY)
        pythoncom.CoInitialize()

        excel = win32.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        registrar_log("📂  Abrindo planilha de query...")
        wb = excel.Workbooks.Open(
            ARQUIVO_QUERY, UpdateLinks=0, ReadOnly=False,
            IgnoreReadOnlyRecommended=True, Notify=False
        )

        if wb.ReadOnly:
            registrar_log("⚠️  Abriu como leitura. Tentando destravar...", "aviso")
            try:
                # Mode=3 = xlExclusive > força escrita quando o arquivo abriu como somente leitura.
                wb.ChangeFileAccess(Mode=3)
            except Exception:
                registrar_log("❌  Falha ao destravar. Arquivo bloqueado na rede.", "erro")
                wb.Close(SaveChanges=False)
                return "erro", None

        try:
            # FastCombine ignora os níveis de privacidade da query > sem isso, o Excel para pedindo confirmação manual.
            wb.Queries.FastCombine = True
        except Exception as e:
            registrar_log(f"⚠️  Falha ao ativar Fast Combine (ignorar privacidade): {e}", "aviso")

        ws_config = wb.Sheets(ABA_CONFIGURACOES)
        ws_config.Range(CELULA_DATA_ALVO).NumberFormat = "@"
        ws_config.Range(CELULA_DATA_ALVO).Value = str(data_texto)
        ws_config.Range(CELULA_SETOR_ALVO).Value = setor
        registrar_log("✍️  Dados colados na query.")

        # BackgroundQuery desligado > o código só segue depois que o RefreshAll termina.
        for connection in wb.Connections:
            try:
                connection.OLEDBConnection.BackgroundQuery = False
            except Exception:
                pass

        registrar_log("🔄  Atualizando query...")
        wb.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()
        time.sleep(5)

        registrar_log("🔍  Validando se a query trouxe os dados corretos...")
        ws_aprova = wb.Sheets(ABA_APROVACAO)
        data_query  = ws_aprova.Cells(2, 3).Value
        setor_query = ws_aprova.Cells(2, 6).Value

        data_query_str = ""
        if data_query is not None:
            try:
                data_query_str = data_query.strftime("%d/%m/%Y")
            except AttributeError:
                data_query_str = str(data_query).strip()[:10]
        setor_query_str = str(setor_query).strip().upper() if setor_query else ""
        setor_alvo_str  = str(setor).strip().upper()

        if data_query_str != str(data_texto) or setor_query_str != setor_alvo_str:
            registrar_log(
                f"❌  A query não atualizou! Esperado: [{data_texto} | {setor_alvo_str}] "
                f"-- Retornou: [{data_query_str} | {setor_query_str}]", "erro"
            )
            wb.Close(SaveChanges=False)
            return "erro", None

        registrar_log("✅  Query validada com sucesso!", "ok")

        # Coluna T recebe a fórmula da linha 2; sem fórmula na linha 2, usa o backup da coluna Y.
        registrar_log("📝  Ajustando fórmula da coluna T...")
        ultima_linha = ws_aprova.Cells(ws_aprova.Rows.Count, 2).End(-4162).Row
        if ultima_linha >= 2:
            formula_t2 = ws_aprova.Cells(2, 20).Formula
            if not formula_t2 or str(formula_t2).strip() == "":
                registrar_log("⚠️  Fórmula ausente na coluna T. Puxando backup da coluna Y...", "aviso")
                ws_aprova.Cells(2, 20).Formula = ws_aprova.Cells(2, 25).Formula
            if ultima_linha > 2:
                for i in range(3, ultima_linha + 1):
                    ws_aprova.Cells(i, 20).Formula = ws_aprova.Cells(2, 20).Formula
            registrar_log(f"✅  Fórmulas aplicadas até a linha {ultima_linha}", "ok")


        # Coluna T: CDA ou FORA CDA > outro valor indica fornecedor sem mapeamento.
        registrar_log("🔎  Verificando se todos os fornecedores estão mapeados...")
        col_fornecedor = _achar_coluna_cabecalho(ws_aprova, "FORNECEDOR")
        fornecedores_com_problema = set()
        if ultima_linha >= 2:
            for i in range(2, ultima_linha + 1):
                valor_t = str(ws_aprova.Cells(i, 20).Value or "").strip().upper()
                if valor_t not in ("CDA", "FORA CDA"):
                    nome_forn = ""
                    if col_fornecedor:
                        nome_forn = str(ws_aprova.Cells(i, col_fornecedor).Value or "").strip()
                    fornecedores_com_problema.add(nome_forn or f"(linha {i} sem nome de fornecedor)")

        if fornecedores_com_problema:
            registrar_log(
                f"⚠️  {len(fornecedores_com_problema)} fornecedor(es) não mapeado(s) -- "
                f"corrija antes de prosseguir.", "aviso"
            )
            wb.Close(SaveChanges=False)
            return "fornecedor_pendente", sorted(fornecedores_com_problema)

        registrar_log("✅  Todos os fornecedores estão mapeados.", "ok")

        registrar_log("💾  Salvando...")
        wb.Save()
        registrar_log("✅  Query salva com sucesso!", "ok")
        return "ok", None

    except Exception as e:
        registrar_log(f"❌  Erro no Excel: {e}", "erro")
        registrar_erro_permanente(f"QUERY -- {e}")
        return "erro", None
    finally:
        if wb:
            try:
                wb.Close(SaveChanges=False)
            except Exception:
                pass
        if excel:
            try:
                excel.Quit()
            except Exception:
                pass
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

def copiar_para_fila_aprovacao():
    try:
        registrar_log("🚚  Copiando para a fila do Aprovador...")
        os.makedirs(os.path.dirname(CAMINHO_FILA), exist_ok=True)


        shutil.copy(ARQUIVO_QUERY, CAMINHO_FILA)
        registrar_log("✅  Copiado com sucesso!", "ok")
        return True
    except Exception as e:
        registrar_log(f"❌  Erro ao copiar: {e}", "erro")
        registrar_erro_permanente(f"CÓPIA PARA FILA -- {e}")
        return False


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# JANELA DO PREPARADOR
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
class JanelaPreparador:
    FONTE_TITULO   = ("Segoe UI", 17, "bold")
    FONTE_SUB      = ("Segoe UI", 12)
    FONTE_ROTULO   = ("Segoe UI", 10, "bold")
    FONTE_TEXTO    = ("Segoe UI", 13)
    FONTE_PEQUENA  = ("Segoe UI", 10)
    FONTE_MONO     = ("Consolas", 10)

    ICONES_LOG = {"ok": "✅", "aviso": "⚠️", "erro": "❌", "normal": "🔹"}
    TINTS_LOG  = {
        "ok":     COR_OK_FUNDO,
        "aviso":  COR_AVISO_FUNDO,
        "erro":   COR_ERRO_FUNDO,
        "normal": None,
    }

    def __init__(self):
        _gerenciar_log()
        _definir_callback_log(self._log_na_tela)

        self.estado = "verificando"
        self._parar_heartbeat  = threading.Event()
        self._seguir_manual    = False
        self._mtime_status_antes = None

        self.root = ctk.CTk()
        self.root.title("Robô Preparador")
        self.root.configure(fg_color=COR_FUNDO)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        self.setor_selecionado = tk.StringVar(master=self.root, value="")


        self._construir_ui_boot()
        self._centralizar(560, 680)
        self._renderizar_estado()
        self.root.mainloop()

    def _centralizar(self, w, h):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _cabecalho(self, parent, subtitulo):
        hdr = ctk.CTkFrame(parent, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(24, 16))

        badge = ctk.CTkLabel(hdr, text="📄", font=("Segoe UI", 20),
                             fg_color=COR_HEADER, text_color=COR_HEADER_TXT,
                             corner_radius=12, width=44, height=44)
        badge.pack(side="left")

        txt_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        txt_hdr.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(txt_hdr, text="Robô Preparador", font=self.FONTE_TITULO,
                    text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(txt_hdr, text=subtitulo, font=self.FONTE_SUB,
                    text_color=COR_DETALHE, anchor="w").pack(anchor="w")

        credito = ctk.CTkButton(
            hdr, text=f"👤  CRIADO POR: {NOME_CRIADOR}", font=("Segoe UI", 9),
            fg_color="transparent", text_color=COR_MUTED, hover_color=COR_CARD,
            corner_radius=6, height=22, anchor="e",
            command=lambda: webbrowser.open(LINK_GITHUB_CRIADOR)
        )
        credito.pack(side="right", anchor="n")
        return hdr


    def _construir_ui_boot(self):
        self._cabecalho(self.root, "Preparando o ambiente...")

        self.frm_controle = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frm_controle.pack(fill="both", expand=True, padx=24)

        frm_rodape = ctk.CTkFrame(self.root, fg_color="transparent")
        frm_rodape.pack(fill="x", padx=24, pady=(4, 20))
        ctk.CTkButton(frm_rodape, text="✖  Fechar", font=self.FONTE_PEQUENA,
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, width=100, height=32,
                     command=self._ao_fechar).pack(side="right")

    def _entrar_no_app(self):
        for w in self.root.winfo_children():
            w.destroy()
        self._construir_ui_principal()
        self.estado = "pronto"
        self._renderizar_estado()


    def _construir_ui_principal(self):
        self._cabecalho(self.root, "Preparação de pedidos para aprovação")


        self.frm_controle = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frm_controle.pack(fill="x", padx=24)


        frm_hist_wrap = ctk.CTkFrame(self.root, fg_color="transparent")
        frm_hist_wrap.pack(fill="both", expand=True, padx=24, pady=(16, 8))

        cab_hist = ctk.CTkFrame(frm_hist_wrap, fg_color="transparent")
        cab_hist.pack(fill="x")
        ctk.CTkLabel(cab_hist, text="HISTÓRICO", font=("Segoe UI", 10, "bold"),
                    text_color=COR_MUTED, anchor="w").pack(side="left")
        ctk.CTkLabel(cab_hist, text="● ao vivo", font=("Segoe UI", 9),
                    text_color=COR_OK, anchor="e").pack(side="right")

        self.frm_log = ctk.CTkScrollableFrame(frm_hist_wrap, fg_color=COR_CARD,
                                              corner_radius=12, border_width=1,
                                              border_color=COR_BORDA, height=230)
        self.frm_log.pack(fill="both", expand=True, pady=(6, 0))


        frm_rodape = ctk.CTkFrame(self.root, fg_color="transparent")
        frm_rodape.pack(fill="x", padx=24, pady=(4, 20))
        ctk.CTkButton(frm_rodape, text="✖  Fechar", font=self.FONTE_PEQUENA,
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, width=100, height=32,
                     command=self._ao_fechar).pack(side="right")

    def _log_na_tela(self, mensagem, hora, tag="normal"):
        def _run():
            try:
                icone = self.ICONES_LOG.get(tag, "🔹")
                tint  = self.TINTS_LOG.get(tag)
                linha = ctk.CTkFrame(self.frm_log, fg_color=(tint or "transparent"),
                                     corner_radius=8)
                linha.pack(fill="x", padx=4, pady=3)

                conteudo = ctk.CTkFrame(linha, fg_color="transparent")
                conteudo.pack(fill="x", padx=8, pady=6)

                ctk.CTkLabel(conteudo, text=icone, font=("Segoe UI", 12),
                            width=20).pack(side="left", anchor="n")

                txt_col = ctk.CTkFrame(conteudo, fg_color="transparent")
                txt_col.pack(side="left", fill="x", expand=True, padx=(6, 0))
                ctk.CTkLabel(txt_col, text=mensagem, font=self.FONTE_PEQUENA,
                            text_color=COR_TEXTO, anchor="w", justify="left",
                            wraplength=440).pack(anchor="w")
                ctk.CTkLabel(txt_col, text=hora, font=("Consolas", 9),
                            text_color=COR_MUTED, anchor="w").pack(anchor="w")

                self.root.after(50, lambda: self.frm_log._parent_canvas.yview_moveto(1.0))
            except Exception:
                pass
        try:
            self.root.after(0, _run)
        except Exception:
            pass

    def _limpar_controle(self):
        for w in self.frm_controle.winfo_children():
            w.destroy()

    def _card(self, titulo=None):
        card = ctk.CTkFrame(self.frm_controle, fg_color=COR_CARD, corner_radius=12,
                            border_width=1, border_color=COR_BORDA)
        card.pack(fill="x", pady=(0, 12))
        interno = ctk.CTkFrame(card, fg_color="transparent")
        interno.pack(fill="x", padx=16, pady=14)
        if titulo:
            ctk.CTkLabel(interno, text=titulo.upper(), font=("Segoe UI", 10, "bold"),
                        text_color=COR_MUTED, anchor="w").pack(anchor="w", pady=(0, 8))
        return interno


    def _renderizar_estado(self):
        self._limpar_controle()
        if self.estado == "verificando":
            self._tela_verificando()
        elif self.estado == "pronto":
            self._tela_pronto()
        elif self.estado == "bloqueado":
            self._tela_bloqueado()
        elif self.estado == "processando":
            self._tela_processando()
        elif self.estado == "revisar_fornecedores":
            self._tela_revisar_fornecedores()
        elif self.estado == "aguardando":
            self._tela_aguardando()
        elif self.estado == "concluido":
            self._tela_concluido()
        elif self.estado == "erro_aprovador":
            self._tela_erro_aprovador()


    def _tela_verificando(self):
        card = self._card("Bibliotecas")
        self._frm_bibliotecas = ctk.CTkFrame(card, fg_color="transparent")
        self._frm_bibliotecas.pack(fill="x")

        self._lbl_status_geral = ctk.CTkLabel(card, text="Verificando...", font=("Segoe UI", 10),
                                              text_color=COR_MUTED, anchor="w")
        self._lbl_status_geral.pack(fill="x", pady=(10, 4))

        self._barra_progresso = ctk.CTkProgressBar(card, height=6, corner_radius=4,
                                                    fg_color=COR_BORDA, progress_color=COR_HEADER)
        self._barra_progresso.set(0)
        self._barra_progresso.pack(fill="x")
        threading.Thread(target=self._checar_ambiente, daemon=True).start()

    def _status_geral(self, texto):
        try:
            self.root.after(0, lambda: self._lbl_status_geral.configure(text=texto))
        except Exception:
            pass

    def _fade_in_label(self, widget, cor_final, passos=10, intervalo=18):
        def _hex_rgb(c):
            c = c.lstrip("#")
            return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        r1, g1, b1 = _hex_rgb(COR_CARD)
        r2, g2, b2 = _hex_rgb(cor_final)
        def _tick(i=0):
            if i > passos:
                try:
                    widget.configure(text_color=cor_final)
                except Exception:
                    pass
                return
            frac = i / passos
            cor = "#{:02X}{:02X}{:02X}".format(
                int(r1 + (r2 - r1) * frac), int(g1 + (g2 - g1) * frac), int(b1 + (b2 - b1) * frac))
            try:
                widget.configure(text_color=cor)
            except Exception:
                return
            self.root.after(intervalo, lambda: _tick(i + 1))
        _tick()

    def _linha_biblioteca(self, nome, estado="instalando"):
        resultado = {}
        evento = threading.Event()
        def _run():
            try:
                linha = ctk.CTkFrame(self._frm_bibliotecas, fg_color="transparent")
                linha.pack(fill="x")
                interno = ctk.CTkFrame(linha, fg_color="transparent")
                interno.pack(fill="x", pady=8)

                canvas_icone = tk.Canvas(interno, width=16, height=16, bg=COR_CARD,
                                         highlightthickness=0)
                canvas_icone.pack(side="left", padx=(0, 8))

                lbl_nome = ctk.CTkLabel(interno, text=nome, font=("Segoe UI", 12),
                                        text_color=COR_CARD)
                lbl_nome.pack(side="left")

                lbl_resultado = ctk.CTkLabel(interno, text="", font=("Segoe UI", 13, "bold"),
                                             text_color=COR_CARD)
                lbl_resultado.pack(side="right")

                ctk.CTkFrame(self._frm_bibliotecas, fg_color=COR_BORDA, height=1).pack(fill="x")

                resultado["canvas_icone"] = canvas_icone
                resultado["lbl_nome"] = lbl_nome
                resultado["lbl_resultado"] = lbl_resultado
                resultado["spinner_ativo"] = {"ativo": False}

                self._fade_in_label(lbl_nome, COR_TEXTO)
            except Exception:
                pass
            evento.set()
        try:
            self.root.after(0, _run)
        except Exception:
            evento.set()
        evento.wait(timeout=2)
        if resultado:
            self._definir_estado_linha(resultado, estado)
        return resultado

    def _girar_spinner(self, canvas_spinner, ativo_ref):
        angulo = [0]
        def _tick():
            if not ativo_ref["ativo"] or not canvas_spinner:
                return
            angulo[0] = (angulo[0] + 24) % 360
            try:
                canvas_spinner.itemconfig("arco", start=angulo[0])
            except Exception:
                return
            self.root.after(40, _tick)
        try:
            self.root.after(0, _tick)
        except Exception:
            pass

    def _definir_estado_linha(self, referencia, estado):
        def _run():
            try:
                canvas = referencia["canvas_icone"]
                referencia["spinner_ativo"]["ativo"] = False
                canvas.delete("all")

                if estado == "instalando":
                    canvas.create_arc(2, 2, 14, 14, start=0, extent=270, style="arc",
                                      outline=COR_HEADER, width=2, tags="arco")
                    referencia["spinner_ativo"]["ativo"] = True
                    self._girar_spinner(canvas, referencia["spinner_ativo"])
                else:

                    canvas.create_oval(2, 2, 14, 14, outline=COR_HEADER, width=2)

                if estado in ("ok", "instalado"):
                    referencia["lbl_resultado"].configure(text="✓", text_color=COR_OK)
                elif estado == "erro":
                    referencia["lbl_resultado"].configure(text="✕", text_color=COR_ERRO)
            except Exception:
                pass
        try:
            self.root.after(0, _run)
        except Exception:
            pass

    def _mostrar_proximo_verificando(self):
        frm = ctk.CTkFrame(self.frm_controle, fg_color="transparent")
        frm.pack(fill="x", pady=(14, 0))
        if _IMPORTS_OK:
            ctk.CTkLabel(frm, text="Próximo: escolher data e setor do pedido",
                        font=("Segoe UI", 10), text_color=COR_MUTED).pack(anchor="w", pady=(0, 6))
            ctk.CTkButton(frm, text="Continuar  →", font=("Segoe UI", 12, "bold"),
                         fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                         corner_radius=8, height=38,
                         command=self._entrar_no_app).pack(fill="x")
        else:
            ctk.CTkLabel(frm, text=f"❌  Erro: {_IMPORTS_ERRO[:150]}", font=("Segoe UI", 10),
                        text_color=COR_ERRO, wraplength=460, justify="left").pack(anchor="w", pady=(0, 8))
            ctk.CTkLabel(frm, text="Algumas bibliotecas (como pywin32) só funcionam de "
                                  "verdade depois de reiniciar o programa.",
                        font=("Segoe UI", 9), text_color=COR_MUTED,
                        wraplength=460, justify="left").pack(anchor="w", pady=(0, 8))
            ctk.CTkButton(frm, text="🔄  Reiniciar", font=("Segoe UI", 11, "bold"),
                         fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO, hover_color=COR_BORDA,
                         corner_radius=8, height=36,
                         command=self._reiniciar_programa).pack(fill="x")

    def _reiniciar_programa(self):
        try:
            subprocess.Popen([sys.executable, os.path.abspath(__file__)])
        except Exception as e:
            registrar_erro_permanente(f"REINICIAR -- {e}")
        finally:
            try:
                self.root.destroy()
            except Exception:
                pass
            os._exit(0)

    def _checar_ambiente(self):
        total = len(_STATUS_INSTALL)
        prontas = 0

        def _atualizar_progresso():
            try:
                self.root.after(0, lambda: self._barra_progresso.set(prontas / total if total else 1))
            except Exception:
                pass

        pendentes = []
        for nome_pip, status in _STATUS_INSTALL.items():
            if status == "ok":
                self._status_geral(f"Verificando {nome_pip}...")
                self._linha_biblioteca(nome_pip, "ok")
                prontas += 1
                _atualizar_progresso()
                time.sleep(0.35)
            else:
                pendentes.append(nome_pip)

        for nome_pip in pendentes:
            modulo = next((ni for ni, np in _LIBS if np == nome_pip), nome_pip)
            self._status_geral(f"Instalando {nome_pip}...")
            referencia = self._linha_biblioteca(nome_pip, "instalando")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", nome_pip, "--quiet"],
                               capture_output=True, timeout=180, creationflags=_NO_WINDOW)


                importlib.invalidate_caches()
                if nome_pip == "pywin32":
                    _corrigir_dll_pywin32()
                __import__(modulo)
                _STATUS_INSTALL[nome_pip] = "ok"
                self._definir_estado_linha(referencia, "instalado")
                self._status_geral(f"{nome_pip} instalado!")
            except Exception as e_lib:
                _STATUS_INSTALL[nome_pip] = "erro"
                self._definir_estado_linha(referencia, "erro")
                self._status_geral(f"Falha ao instalar {nome_pip}")
                registrar_erro_permanente(f"INSTALAR {nome_pip} -- {e_lib}")
            prontas += 1
            _atualizar_progresso()
            time.sleep(0.2)

        if not _IMPORTS_OK:
            _tentar_importar_reais()
            if _IMPORTS_OK:
                try:
                    load_dotenv(dotenv_path=CAMINHO_ENV)
                except Exception:
                    pass

        self._status_geral("Tudo pronto!" if _IMPORTS_OK else "Há um problema a resolver.")
        self.root.after(500, self._mostrar_proximo_verificando)


    def _tela_pronto(self):
        card_data = self._card("Data do pedido")
        linha_data = ctk.CTkFrame(card_data, fg_color="transparent")
        linha_data.pack(fill="x")

        self.var_data = tk.StringVar(master=self.root, value=getattr(self, "_ultima_data", ""))
        ctk.CTkLabel(linha_data, text="📅", font=("Segoe UI", 14),
                    text_color="#B8860B", width=20).pack(side="left", padx=(0, 8))
        ent_data = ctk.CTkEntry(linha_data, textvariable=self.var_data,
                                font=self.FONTE_TEXTO, fg_color=COR_FUNDO,
                                border_width=1, border_color=COR_BORDA,
                                text_color=COR_TEXTO, corner_radius=8,
                                width=160, height=34, placeholder_text="dd/mm/aaaa")
        ent_data.pack(side="left")
        self.var_data.trace_add("write", lambda *a: self._validar_pronto())

        ctk.CTkButton(linha_data, text="📆 Escolher", font=self.FONTE_PEQUENA,
                     fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO,
                     hover_color=COR_BORDA, corner_radius=8, width=90, height=34,
                     command=self._abrir_calendario).pack(side="left", padx=(8, 0))

        card_setor = self._card("Setor")
        frm_setores = ctk.CTkFrame(card_setor, fg_color="transparent")
        frm_setores.pack(fill="x")
        self._botoes_setor = {}
        icones_setor = {"ELETRO-ELETRONICOS": "💡", "BELEZA": "✨"}
        for nome in SETORES_DISPONIVEIS:
            b = ctk.CTkButton(
                frm_setores, text=f"{icones_setor.get(nome, '🏷')}\n{nome.title()}",
                font=self.FONTE_PEQUENA, fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO,
                hover_color=COR_BORDA, corner_radius=10, height=64,
                command=lambda n=nome: self._selecionar_setor(n)
            )
            b.pack(side="left", expand=True, fill="x", padx=4)
            self._botoes_setor[nome] = b
        if self.setor_selecionado.get():
            self._selecionar_setor(self.setor_selecionado.get())

        self.btn_processar = ctk.CTkButton(
            self.frm_controle, text="▶  Processar", font=("Segoe UI", 14, "bold"),
            fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
            text_color_disabled=COR_HEADER_TXT,
            corner_radius=10, height=46, state="disabled",
            command=self._iniciar_processamento
        )
        self.btn_processar.pack(fill="x", pady=(4, 0))

        self._validar_pronto()

    def _abrir_calendario(self):
        top = ctk.CTkToplevel(self.root)
        top.title("Escolher data")
        top.resizable(False, False)
        top.attributes("-topmost", True)
        try:
            data_inicial = datetime.strptime(self.var_data.get(), "%d/%m/%Y")
        except Exception:
            data_inicial = datetime.now()
        cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy",
                       year=data_inicial.year, month=data_inicial.month,
                       day=data_inicial.day, locale="pt_BR")
        cal.pack(padx=12, pady=12)

        def _confirmar():
            self.var_data.set(cal.get_date())
            top.destroy()

        ctk.CTkButton(top, text="Confirmar", command=_confirmar,
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT,
                     corner_radius=8).pack(pady=(0, 12))

    def _selecionar_setor(self, nome):
        self.setor_selecionado.set(nome)
        for n, b in self._botoes_setor.items():
            if n == nome:
                b.configure(fg_color=COR_CHIP_ATIVO, text_color=COR_HEADER_TXT,
                           hover_color="#E6B325")
            else:
                b.configure(fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO,
                           hover_color=COR_BORDA)
        self._validar_pronto()

    def _validar_pronto(self):
        data_ok  = bool(self.var_data.get().strip())
        setor_ok = bool(self.setor_selecionado.get())
        pode = data_ok and setor_ok and _IMPORTS_OK
        try:
            self.btn_processar.configure(state="normal" if pode else "disabled")
        except Exception:
            pass


    def _tela_bloqueado(self):
        info = getattr(self, "_info_bloqueio", None) or {}
        card = self._card()
        ctk.CTkLabel(card, text="⏳  Já existe um lote em andamento",
                    font=("Segoe UI", 13, "bold"), text_color=COR_AVISO,
                    anchor="w").pack(anchor="w")
        detalhe = (f"Máquina: {info.get('pc','?')}   |   Iniciado: {info.get('inicio','?')}\n"
                  f"Data: {info.get('data','?')}   |   Setor: {info.get('setor','?')}")
        ctk.CTkLabel(card, text=detalhe, font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    justify="left", anchor="w").pack(anchor="w", pady=(8, 12))
        ctk.CTkButton(card, text="🔄  Verificar novamente", font=self.FONTE_PEQUENA,
                     fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO, hover_color=COR_BORDA,
                     corner_radius=8, height=34,
                     command=lambda: self._mudar_estado("pronto")).pack(anchor="w")


    def _tela_processando(self):
        card = self._card()
        ctk.CTkLabel(card, text="⚙️  Processando...", font=("Segoe UI", 13, "bold"),
                    text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card,
                    text=f"Data: {self.var_data.get()}   |   Setor: {self.setor_selecionado.get()}",
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    anchor="w").pack(anchor="w", pady=(6, 0))
        barra = ctk.CTkProgressBar(card, height=6, corner_radius=4,
                                   fg_color=COR_FUNDO, progress_color=COR_HEADER,
                                   mode="indeterminate")
        barra.pack(fill="x", pady=(12, 0))
        barra.start()


    def _tela_revisar_fornecedores(self):
        card = self._card()
        ctk.CTkLabel(card, text="⚠️  Fornecedores não mapeados encontrados",
                    font=("Segoe UI", 13, "bold"), text_color=COR_ERRO,
                    anchor="w").pack(anchor="w")

        lista_txt = "\n".join(f"•  {f}" for f in getattr(self, "_fornecedores_pendentes", []))
        ctk.CTkLabel(card, text=lista_txt, font=self.FONTE_PEQUENA, text_color=COR_TEXTO,
                    justify="left", anchor="w", wraplength=460).pack(anchor="w", pady=(8, 6))

        ctk.CTkLabel(card,
                    text="Corrija esses fornecedores na planilha de mapeamento antes de continuar.",
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    wraplength=460, justify="left", anchor="w").pack(anchor="w", pady=(0, 12))

        frm_btns = ctk.CTkFrame(card, fg_color="transparent")
        frm_btns.pack(fill="x")
        ctk.CTkButton(frm_btns, text="📂  Abrir planilha", font=self.FONTE_PEQUENA,
                     fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO, hover_color=COR_BORDA,
                     corner_radius=8, height=34,
                     command=self._abrir_planilha_fornecedores).pack(side="left", padx=(0, 8))
        ctk.CTkButton(frm_btns, text="✅  Corrigi, atualizar", font=("Segoe UI", 11, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=8, height=34,
                     command=self._corrigir_e_atualizar).pack(side="left", padx=(0, 8))
        ctk.CTkButton(frm_btns, text="✖  Cancelar", font=self.FONTE_PEQUENA,
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                     corner_radius=8, height=34,
                     command=self._cancelar_revisao).pack(side="left")

    def _abrir_planilha_fornecedores(self):
        try:
            os.startfile(CAMINHO_FORNECEDORES)
        except Exception as e:
            registrar_log(f"❌  Falha ao abrir a planilha de fornecedores: {e}", "erro")
            registrar_erro_permanente(f"ABRIR FORNECEDORES -- {e}")

    def _corrigir_e_atualizar(self):
        data_texto, setor = self._dados_pendentes
        registrar_log("🔄  Atualizando novamente após correção manual...")
        self.estado = "processando"
        self._renderizar_estado()
        threading.Thread(target=self._executar_fluxo, args=(data_texto, setor), daemon=True).start()

    def _cancelar_revisao(self):
        registrar_log("✖  Revisão de fornecedores cancelada pelo usuário.", "aviso")
        self._parar_heartbeat.set()
        _liberar_lock()
        self._mudar_estado("pronto")


    def _tela_aguardando(self):
        card = self._card()
        ctk.CTkLabel(card, text="⏳  Aguardando aprovação...", font=("Segoe UI", 13, "bold"),
                    text_color=COR_AVISO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card,
                    text=f"Data: {self.var_data.get()}   |   Setor: {self.setor_selecionado.get()}",
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    anchor="w").pack(anchor="w", pady=(6, 4))
        self.lbl_timer = ctk.CTkLabel(card, text="Tempo decorrido: 0min 0s",
                                      font=self.FONTE_PEQUENA, text_color=COR_MUTED, anchor="w")
        self.lbl_timer.pack(anchor="w", pady=(0, 12))
        ctk.CTkButton(card, text="⏭  Seguir mesmo assim", font=self.FONTE_PEQUENA,
                     fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO, hover_color=COR_BORDA,
                     corner_radius=8, height=34,
                     command=self._seguir_mesmo_assim).pack(anchor="w")
        self._inicio_espera = time.time()
        self._tick_timer()

    def _tick_timer(self):
        if self.estado != "aguardando":
            return
        decorrido = int(time.time() - self._inicio_espera)
        try:
            self.lbl_timer.configure(text=f"Tempo decorrido: {decorrido//60}min {decorrido%60}s")
        except Exception:
            return
        self.root.after(1000, self._tick_timer)


    def _tela_concluido(self):
        card = self._card()
        ctk.CTkLabel(card, text="✅  Aprovação concluída!", font=("Segoe UI", 14, "bold"),
                    text_color=COR_OK, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card,
                    text=f"Data: {self.var_data.get()}   |   Setor: {self.setor_selecionado.get()}",
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    anchor="w").pack(anchor="w", pady=(6, 12))
        ctk.CTkButton(self.frm_controle, text="🔄  Processar nova data",
                     font=("Segoe UI", 14, "bold"), fg_color=COR_HEADER,
                     text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=10, height=46,
                     command=self._resetar_para_nova_data).pack(fill="x")
        ctk.CTkButton(self.frm_controle, text="🔁  Processar mesma data novamente",
                     font=self.FONTE_PEQUENA, fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, height=34,
                     command=self._perguntar_reenvio).pack(fill="x", pady=(8, 0))


    def _tela_erro_aprovador(self):
        card = self._card()
        ctk.CTkLabel(card, text="⚠️  Erro no Aprovador -- verificar antes de processar uma nova data",
                    font=("Segoe UI", 14, "bold"), text_color=COR_AVISO, anchor="w",
                    wraplength=460, justify="left").pack(anchor="w")
        motivo = getattr(self, "_info_bloqueio", "") or ""
        if motivo:
            ctk.CTkLabel(card, text=motivo, font=self.FONTE_PEQUENA, text_color=COR_MUTED,
                        anchor="w", wraplength=460, justify="left").pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(card,
                    text=f"Data: {self.var_data.get()}   |   Setor: {self.setor_selecionado.get()}",
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    anchor="w").pack(anchor="w", pady=(6, 12))
        ctk.CTkButton(self.frm_controle, text="🔄  Processar nova data",
                     font=("Segoe UI", 14, "bold"), fg_color=COR_HEADER,
                     text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=10, height=46,
                     command=self._resetar_para_nova_data).pack(fill="x")
        ctk.CTkButton(self.frm_controle, text="🔁  Processar mesma data novamente",
                     font=self.FONTE_PEQUENA, fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, height=34,
                     command=self._perguntar_reenvio).pack(fill="x", pady=(8, 0))


    def _mudar_estado(self, novo, info=None):
        self.estado = novo
        if info is not None:
            self._info_bloqueio = info
        self._renderizar_estado()

    def _iniciar_processamento(self):
        data_texto = self.var_data.get().strip()
        setor      = self.setor_selecionado.get()

        try:
            datetime.strptime(data_texto, "%d/%m/%Y")
        except Exception:
            registrar_log("❌  Data em formato inválido. Use dd/mm/aaaa.", "erro")
            return

        obtido, info = _tentar_obter_lock(data_texto, setor)
        if not obtido:
            self._mudar_estado("bloqueado", info=info)
            return

        self._ultima_data = data_texto
        self._parar_heartbeat.clear()
        self._seguir_manual = False
        self.estado = "processando"
        self._renderizar_estado()

        threading.Thread(target=self._executar_fluxo, args=(data_texto, setor), daemon=True).start()
        threading.Thread(target=self._loop_heartbeat, daemon=True).start()

    def _perguntar_reenvio(self):
        data_texto = getattr(self, "_ultima_data", "")
        setor = self.setor_selecionado.get()
        import tkinter.messagebox as _mb
        confirmar = _mb.askyesno(
            "Processar novamente",
            f"Tem certeza que quer processar a data {data_texto} ({setor}) novamente?\n\n"
            "Isso reenvia o arquivo já preparado direto para o Aprovador, "
            "SEM atualizar a query de novo."
        )
        if confirmar:
            self._iniciar_reenvio(data_texto, setor)

    def _iniciar_reenvio(self, data_texto, setor):
        obtido, info = _tentar_obter_lock(data_texto, setor)
        if not obtido:
            self._mudar_estado("bloqueado", info=info)
            return

        self._parar_heartbeat.clear()
        self._seguir_manual = False
        self.estado = "processando"
        self._renderizar_estado()

        threading.Thread(target=self._executar_reenvio, args=(data_texto, setor), daemon=True).start()
        threading.Thread(target=self._loop_heartbeat, daemon=True).start()

    def _executar_reenvio(self, data_texto, setor):
        registrar_log(f"🔁  Reenviando o mesmo arquivo (sem atualizar a query) -- "
                      f"Data: {data_texto} | Setor: {setor}")

        if not os.path.exists(ARQUIVO_QUERY):
            registrar_log("❌  Arquivo de query não encontrado. Não é possível reenviar.", "erro")
            self._parar_heartbeat.set()
            _liberar_lock()
            self.root.after(0, lambda: self._mudar_estado("pronto"))
            return

        if not copiar_para_fila_aprovacao():
            self._parar_heartbeat.set()
            _liberar_lock()
            self.root.after(0, lambda: self._mudar_estado("pronto"))
            return

        self._snapshot_mtime_status()
        registrar_log("⏳  Aguardando o Robô Aprovador processar esse lote...", "aviso")
        self.root.after(0, lambda: self._mudar_estado("aguardando"))
        threading.Thread(target=self._loop_espera_aprovacao, daemon=True).start()

    def _snapshot_mtime_status(self):

        try:
            self._mtime_status_antes = os.path.getmtime(CAMINHO_STATUS_APROVADOR)
        except Exception:
            self._mtime_status_antes = None

    def _loop_heartbeat(self):
        while not self._parar_heartbeat.wait(HEARTBEAT_INTERVALO):
            _atualizar_heartbeat_lock()

    def _executar_fluxo(self, data_texto, setor):
        _gerenciar_log()
        registrar_log(f"🌐  Iniciando processamento -- Data: {data_texto} | Setor: {setor}")

        status, dados = atualizar_query(data_texto, setor)

        if status == "fornecedor_pendente":
            self._fornecedores_pendentes = dados
            self._dados_pendentes = (data_texto, setor)
            self.root.after(0, lambda: self._mudar_estado("revisar_fornecedores"))
            return

        if status != "ok":
            self._parar_heartbeat.set()
            _liberar_lock()
            self.root.after(0, lambda: self._mudar_estado("pronto"))
            return

        if not copiar_para_fila_aprovacao():
            self._parar_heartbeat.set()
            _liberar_lock()
            self.root.after(0, lambda: self._mudar_estado("pronto"))
            return

        self._snapshot_mtime_status()
        registrar_log("⏳  Aguardando o Robô Aprovador processar esse lote...", "aviso")
        self.root.after(0, lambda: self._mudar_estado("aguardando"))
        threading.Thread(target=self._loop_espera_aprovacao, daemon=True).start()

    def _loop_espera_aprovacao(self):
        while self.estado == "aguardando" and not self._seguir_manual:
            try:
                if (os.path.exists(CAMINHO_STATUS_APROVADOR)
                        and (self._mtime_status_antes is None
                             or os.path.getmtime(CAMINHO_STATUS_APROVADOR) > self._mtime_status_antes)):
                    with open(CAMINHO_STATUS_APROVADOR, "r", encoding="utf-8") as f:
                        status_txt, _, motivo = f.read().strip().partition("|")
                    self._parar_heartbeat.set()
                    _liberar_lock()
                    if status_txt == "OK":
                        registrar_log("✅  Resultado de aprovação detectado!", "ok")
                        self.root.after(0, lambda: self._mudar_estado("concluido"))
                    else:
                        registrar_log(f"⚠️  Aprovador sinalizou um problema: {motivo}", "erro")
                        self.root.after(0, lambda m=motivo: self._mudar_estado("erro_aprovador", info=m))
                    return
            except Exception:
                pass
            time.sleep(5)

    def _seguir_mesmo_assim(self):
        registrar_log("⏭  Seguindo manualmente, sem confirmação de aprovação.", "aviso")
        self._seguir_manual = True
        self._parar_heartbeat.set()
        _liberar_lock()
        self._mudar_estado("concluido")

    def _resetar_para_nova_data(self):
        self.setor_selecionado.set("")
        self.estado = "pronto"
        self._renderizar_estado()

    def _ao_fechar(self):
        avisos = {
            "processando": (
                "Isso interromperá o processo do Robô Preparador, mas o Robô "
                "Aprovador continuará a atualização (caso não seja interrompido "
                "manualmente).\n\nTem certeza que deseja fechar?"
            ),
            "aguardando": (
                "Isso interromperá o processo do Robô Preparador, mas o Robô "
                "Aprovador continuará a atualização (caso não seja interrompido "
                "manualmente).\n\nTem certeza que deseja fechar?"
            ),
            "revisar_fornecedores": (
                "Ainda há fornecedores não mapeados pendentes de correção. Fechar "
                "agora vai cancelar esse processamento (nada foi enviado para o "
                "Robô Aprovador ainda).\n\nTem certeza que deseja fechar?"
            ),
        }
        if self.estado in avisos:
            import tkinter.messagebox as _mb
            confirmar = _mb.askyesno("Fechar Robô Preparador", avisos[self.estado])
            if not confirmar:
                return
            registrar_log("✖  Janela fechada pelo usuário durante o processo.", "aviso")

        self._parar_heartbeat.set()
        _liberar_lock()
        self.root.destroy()


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# PONTO DE ENTRADA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
if __name__ == "__main__":
    try:
        JanelaPreparador()
    except Exception as _e:


        import traceback
        _erro_completo = traceback.format_exc()
        try:
            with open(os.path.join(pasta_script, "erro_fatal.txt"), "w", encoding="utf-8") as _f:
                _f.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n{_erro_completo}")
        except Exception:
            pass
        try:
            import tkinter.messagebox as _mb
            _raiz_erro = tk.Tk()
            _raiz_erro.withdraw()
            _mb.showerror(
                "Robô Preparador -- Erro ao iniciar",
                f"O robô encontrou um erro e não conseguiu abrir:\n\n{_e}\n\n"
                f"Detalhes salvos em: erro_fatal.txt (nesta mesma pasta)."
            )
            _raiz_erro.destroy()
        except Exception:
            pass
