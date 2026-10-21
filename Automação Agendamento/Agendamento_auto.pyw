# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# BIBLIOTECAS
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
import os
import sys
import time
import glob
import queue
import shutil
import subprocess
import threading
import importlib
import webbrowser
from datetime import datetime, time as dtime

import tkinter as tk

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pasta_script = os.path.dirname(os.path.abspath(__file__))
_NO_WINDOW   = getattr(subprocess, "CREATE_NO_WINDOW", 0)


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# DETECÇÃO PARA AUTO-INSTALAÇÃO DE BIBLIOTECAS
# Instalação ao vivo em _checar_bibliotecas (tela Bibliotecas).
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_LIBS = [
    ("dotenv",        "python-dotenv"),
    ("pystray",       "pystray"),
    ("PIL",           "Pillow"),
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
    _splash.title("Agendamento")
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

def _tentar_importar_reais():
    global _IMPORTS_OK, _IMPORTS_ERRO
    global ctk, load_dotenv
    try:
        import customtkinter as ctk
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    except Exception as _ex:
        _IMPORTS_OK = False
        _IMPORTS_ERRO = f"customtkinter -- {_ex}"
        return

    try:
        from dotenv import load_dotenv
        _IMPORTS_OK = True
        _IMPORTS_ERRO = ""
    except Exception as _ex:
        _IMPORTS_OK = False
        _IMPORTS_ERRO = str(_ex)

_tentar_importar_reais()


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# CONFIGURAÇÕES
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
CAMINHO_ENV = os.path.join(pasta_script, "Config_Cg", ".env")
if _IMPORTS_OK:
    load_dotenv(dotenv_path=CAMINHO_ENV)

ORIGEM_PASTA    = os.getenv("ORIGEM_PASTA",    "")
ORIGEM_PADRAO   = os.getenv("ORIGEM_PADRAO",   "AGENDAMENTO LOGÍSTICA*.xlsm")
NOME_DESTINO    = os.getenv("NOME_DESTINO",    "AGENDAMENTO LOGÍSTICA.xlsm")
DESTINO_PASTA   = os.getenv("DESTINO_PASTA",   "")
MINUTOS_ESPERA  = int(os.getenv("MINUTOS_ESPERA",  "2"))
INTERVALO_CHECK = int(os.getenv("INTERVALO_CHECK", "10"))
MAX_TENTATIVAS  = int(os.getenv("MAX_TENTATIVAS",  "3"))


# Crédito > aparece no canto superior direito do cabeçalho.
NOME_CRIADOR        = os.getenv("NOME_CRIADOR",        "Rhebecca-Taih")
LINK_GITHUB_CRIADOR = os.getenv("LINK_GITHUB_CRIADOR", "https://github.com/Rhebecca-Taih")


# Pausa noturna: encerra às 20h e retoma às 7h30, sem fechar o processo.
HORA_ENCERRAR = dtime(20, 0)
HORA_RETOMAR  = dtime(7, 30)


# Heartbeat a cada 10 min; lock expira após 2h sem atualização > PC travado não prende o lock.
INTERVALO_HEARTBEAT = 10 * 60
EXPIRACAO_LOCK       = 2 * 60 * 60

_status_atual = "Aguardando..."
_parar_loop   = threading.Event()


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
COR_BTN_C        = "#333336"
COR_BTN_C_TXT    = "#F2F2F2"
COR_OK           = "#4ADE80"
COR_OK_FUNDO     = "#173321"
COR_AVISO        = "#FBBF24"
COR_AVISO_FUNDO  = "#3A2E0C"
COR_ERRO         = "#F87171"
COR_ERRO_FUNDO   = "#3A1414"


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

LOG_ARQUIVO          = os.path.join(_pasta_logs,    "log_agendamento.txt")
LOG_ERROS_PERMANENTE = os.path.join(_pasta_logs,    "historico_erros.txt")
LOCK_ARQUIVO         = os.path.join(_pasta_runtime, "agendamento.lock")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOG
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _data_hoje():
    return datetime.now().strftime("%d/%m/%Y")

def _agora_completo():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def _tamanho_formatado(caminho):
    try:
        bytes_ = os.path.getsize(caminho)
        return f"{bytes_ / (1024 * 1024):.2f} MB"
    except Exception:
        return "? MB"

PASTA_LOGS_ANTIGOS = os.path.join(_pasta_logs, "historico_arquivado")
DIAS_MANTER_LOGS_ARQUIVADOS = 30

def _arquivar_log_antigo(segunda_linha):
    try:
        data_str = segunda_linha.split("--")[-1].strip()
        data_arquivo = data_str.replace("/", "-") if data_str else datetime.now().strftime("%d-%m-%Y")
    except Exception:
        data_arquivo = "desconhecida"
    try:
        os.makedirs(PASTA_LOGS_ANTIGOS, exist_ok=True)
        destino = os.path.join(PASTA_LOGS_ANTIGOS, f"log_{data_arquivo}.txt")
        if os.path.exists(destino):
            destino = os.path.join(PASTA_LOGS_ANTIGOS, f"log_{data_arquivo}_{int(time.time())}.txt")
        os.rename(LOG_ARQUIVO, destino)
    except Exception:
        try:
            os.remove(LOG_ARQUIVO)
        except Exception:
            pass

def _limpar_logs_arquivados_antigos():
    try:
        limite = time.time() - DIAS_MANTER_LOGS_ARQUIVADOS * 86400
        for nome in os.listdir(PASTA_LOGS_ANTIGOS):
            caminho = os.path.join(PASTA_LOGS_ANTIGOS, nome)
            if os.path.isfile(caminho) and os.path.getmtime(caminho) < limite:
                os.remove(caminho)
    except Exception:
        pass

def _gerenciar_log():
    sep = "=" * 60
    hoje = _data_hoje()
    if os.path.exists(LOG_ARQUIVO):
        try:
            with open(LOG_ARQUIVO, "r", encoding="utf-8") as f:
                f.readline()
                segunda = f.readline()
            if hoje not in segunda:
                _arquivar_log_antigo(segunda)
                _limpar_logs_arquivados_antigos()
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

PASTA_LOG_LOCAL = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "RobosBureau", "Agendamento")
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

def registrar_log(linhas):
    sep = "-" * 60
    texto_linhas = linhas if isinstance(linhas, list) else [str(linhas)]
    bloco = sep + "\n" + "".join(l + "\n" for l in texto_linhas) + "\n"
    try:
        _gerenciar_log()
        with open(LOG_ARQUIVO, "a", encoding="utf-8") as f:
            aviso = _aviso_rede_restabelecida()
            if aviso:
                f.write(f"{sep}\n{aviso}\n\n")
            f.write(bloco)
        _confirmar_rede_ok()
    except Exception:
        _registrar_log_local(f"[{_agora_completo()}]\n{bloco}")

def registrar_erro_permanente(msg):
    try:
        with open(LOG_ERROS_PERMANENTE, "a", encoding="utf-8") as f:
            f.write(f"[{_agora_completo()}] {msg}\n")
    except Exception:
        _registrar_log_local(f"[{_agora_completo()}] ERRO: {msg}\n")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOCK
# Formato do arquivo: PID|NOME_PC|DATA_INICIO|ULTIMO_HEARTBEAT
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _verificar_instancia_unica():
    nome_pc = os.environ.get("COMPUTERNAME", "DESCONHECIDO")
    if os.path.exists(LOCK_ARQUIVO):
        try:
            with open(LOCK_ARQUIVO, "r") as f:
                partes = f.read().strip().split("|")
            pid_antigo   = int(partes[0])
            pc_antigo    = partes[1] if len(partes) > 1 else "?"
            dt_inicio    = partes[2] if len(partes) > 2 else "?"
            dt_heartbeat = partes[3] if len(partes) > 3 else dt_inicio

            if pc_antigo == nome_pc:
                r = subprocess.run(f'tasklist /FI "PID eq {pid_antigo}" /NH',
                                   shell=True, capture_output=True, text=True,
                                   creationflags=_NO_WINDOW)
                if str(pid_antigo) in r.stdout:
                    return False, f"{pc_antigo} desde {dt_inicio}"
            else:
                try:
                    hb_dt = datetime.strptime(dt_heartbeat, "%d/%m/%Y %H:%M")
                    idade_seg = (datetime.now() - hb_dt).total_seconds()
                except Exception:
                    idade_seg = 0
                if idade_seg < EXPIRACAO_LOCK:
                    minutos_atras = max(0, int(idade_seg // 60))
                    return False, f"{pc_antigo} desde {dt_inicio} (última atividade há {minutos_atras} min)"
        except Exception:
            pass
        try:
            os.remove(LOCK_ARQUIVO)
        except Exception:
            pass
    try:
        agora_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        with open(LOCK_ARQUIVO, "w") as f:
            f.write(f"{os.getpid()}|{nome_pc}|{agora_str}|{agora_str}")
    except Exception:
        pass
    return True, ""

def _atualizar_heartbeat_lock():
    try:
        if not os.path.exists(LOCK_ARQUIVO):
            return
        with open(LOCK_ARQUIVO, "r") as f:
            partes = f.read().strip().split("|")
        if not partes or int(partes[0]) != os.getpid():
            return
        pc     = partes[1] if len(partes) > 1 else os.environ.get("COMPUTERNAME", "DESCONHECIDO")
        inicio = partes[2] if len(partes) > 2 else datetime.now().strftime("%d/%m/%Y %H:%M")
        with open(LOCK_ARQUIVO, "w") as f:
            f.write(f"{os.getpid()}|{pc}|{inicio}|{datetime.now().strftime('%d/%m/%Y %H:%M')}")
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
# LINHAS DE STATUS ESTILIZADAS
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
TAG_ESTILO = {
    "secao":   {"tint": None,             "font": ("Segoe UI", 12, "bold"), "cor": COR_TEXTO,  "indent": 0,  "pady_top": 10},
    "ok":      {"tint": COR_OK_FUNDO,     "font": ("Segoe UI", 11),         "cor": COR_TEXTO,  "indent": 8,  "pady_top": 2},
    "aviso":   {"tint": COR_AVISO_FUNDO,  "font": ("Segoe UI", 11),         "cor": COR_TEXTO,  "indent": 8,  "pady_top": 2},
    "erro":    {"tint": COR_ERRO_FUNDO,   "font": ("Segoe UI", 11),         "cor": COR_TEXTO,  "indent": 8,  "pady_top": 2},
    "detalhe": {"tint": None,             "font": ("Segoe UI", 10),         "cor": COR_MUTED,  "indent": 20, "pady_top": 1},
    "normal":  {"tint": None,             "font": ("Segoe UI", 11),         "cor": COR_TEXTO,  "indent": 8,  "pady_top": 2},
}

def _criar_linha_log(container, texto, tag="normal", wraplength=460):
    if not texto or not texto.strip():
        ctk.CTkFrame(container, fg_color="transparent", height=6).pack(fill="x")
        return None, None
    estilo = TAG_ESTILO.get(tag, TAG_ESTILO["normal"])
    linha = ctk.CTkFrame(container, fg_color=(estilo["tint"] or "transparent"), corner_radius=8)
    linha.pack(fill="x", padx=4, pady=(estilo["pady_top"], 0))
    lbl = ctk.CTkLabel(linha, text=texto.strip(), font=estilo["font"], text_color=estilo["cor"],
                       anchor="w", justify="left", wraplength=wraplength)
    lbl.pack(anchor="w", padx=(estilo["indent"] + 8, 8), pady=6)
    return linha, lbl

def _classificar_bloco(linhas):
    texto = " ".join(linhas).upper()
    if "✅" in texto or "SUCESSO" in texto:
        return "ok"
    if any(e in texto for e in ["❌", "ERRO", "FALHA", "CRITICO"]):
        return "erro"
    if any(e in texto for e in ["⚠️", "AVISO", "ℹ️"]):
        return "aviso"
    return "normal"

def _parsear_blocos_log(texto_bruto):
    sep = "-" * 60
    blocos = []
    for pedaco in texto_bruto.split(sep):
        linhas = [l.rstrip() for l in pedaco.strip("\n").split("\n") if l.strip()]
        if linhas:
            blocos.append(linhas)
    return blocos


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LÓGICA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# Vários arquivos na origem é normal > usa o de modificação mais recente.
def _resolver_origem():
    padrao = os.path.join(ORIGEM_PASTA, ORIGEM_PADRAO)
    try:
        encontrados = glob.glob(padrao)
    except Exception as e:
        return None, f"❌  Erro ao acessar a pasta de origem: {e}"

    if not encontrados:
        msg = (f"❌  Nenhum arquivo encontrado na pasta de origem.\n"
               f"     Pasta: {ORIGEM_PASTA}\n"
               f"     Padrão: {ORIGEM_PADRAO}")
        return None, msg

    mais_recente = max(encontrados, key=os.path.getmtime)

    if len(encontrados) > 1:
        msg = (f"ℹ️  {len(encontrados)} arquivo(s) encontrado(s) -- usando o mais recente:\n"
               f"     {os.path.basename(mais_recente)}")
        return mais_recente, msg

    return mais_recente, None

def _com_timeout(func, *args, timeout_segundos=30, **kwargs):
    resultado = queue.Queue()

    def _trabalho():
        try:
            resultado.put((True, func(*args, **kwargs)))
        except Exception as e:
            resultado.put((False, e))

    threading.Thread(target=_trabalho, daemon=True).start()
    try:
        return resultado.get(timeout=timeout_segundos)
    except queue.Empty:
        return False, TimeoutError(f"sem resposta em {timeout_segundos}s (rede sem resposta)")

def _resolver_origem_com_timeout(timeout_segundos=30):
    ok, resultado = _com_timeout(_resolver_origem, timeout_segundos=timeout_segundos)
    if ok:
        return resultado
    return None, (f"⏱️  A pasta de rede não respondeu em {timeout_segundos}s "
                  f"({resultado}) -- tentando de novo no próximo ciclo.")

# O horário da origem só é atualizado depois do sucesso aqui > falha na cópia é tentada de novo no próximo ciclo.
def _copiar_com_retry(origem, destino_pasta):
    nome_original = os.path.basename(origem)
    destino_final = os.path.join(destino_pasta, NOME_DESTINO)

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        ok_copia, erro_copia = _com_timeout(shutil.copy2, origem, destino_final)
        if not ok_copia:
            if isinstance(erro_copia, PermissionError):
                if tentativa < MAX_TENTATIVAS:
                    time.sleep(30)
                    continue
                return False, f"🔒  Arquivo permaneceu em uso após {MAX_TENTATIVAS} tentativas. Abortando."
            msg = f"❌  Erro/timeout na cópia (tentativa {tentativa}/{MAX_TENTATIVAS}): {erro_copia}"
            if tentativa < MAX_TENTATIVAS:
                time.sleep(5)
                continue
            return False, msg

        ok_tam_o, tam_origem  = _com_timeout(os.path.getsize, origem)
        ok_tam_d, tam_destino = _com_timeout(os.path.getsize, destino_final)
        if not ok_tam_o or not ok_tam_d:
            msg = f"⏱️  Falha ao confirmar o tamanho após a cópia (tentativa {tentativa}/{MAX_TENTATIVAS})."
            if tentativa < MAX_TENTATIVAS:
                time.sleep(5)
                continue
            return False, msg

        if tam_origem != tam_destino:
            msg = (f"⚠️  Cópia incompleta (tentativa {tentativa}/{MAX_TENTATIVAS}).\n"
                   f"     Origem:  {_tamanho_formatado(origem)}\n"
                   f"     Destino: {_tamanho_formatado(destino_final)}")
            if tentativa < MAX_TENTATIVAS:
                time.sleep(5)
                continue
            return False, msg

        msg = (f"✅  Copiado com sucesso.\n"
               f"     Original: {nome_original}\n"
               f"     Salvo como: {NOME_DESTINO}\n"
               f"     Tamanho:  {_tamanho_formatado(destino_final)}\n"
               f"     Destino:  {destino_pasta}")
        return True, msg

    return False, f"❌  Falha após {MAX_TENTATIVAS} tentativas."


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# JANELA DE LANÇAMENTO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
class JanelaLancamento:
    def __init__(self):
        self.aprovado      = False
        self._falha_lib    = False
        self._falha_pastas = False

        self.root = ctk.CTk()
        self.root.title("Agendamento")
        self.root.configure(fg_color=COR_FUNDO)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._fechar)

        self._construir_ui()
        self._centralizar(560, 620)
        threading.Thread(target=self._verificar_lock_inicial, daemon=True).start()
        self.root.mainloop()

    def _centralizar(self, w, h):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _construir_ui(self):
        hdr = ctk.CTkFrame(self.root, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(24, 16))

        badge = ctk.CTkLabel(hdr, text="👀", font=("Segoe UI", 20),
                             fg_color=COR_HEADER, text_color=COR_HEADER_TXT,
                             corner_radius=12, width=44, height=44)
        badge.pack(side="left")

        txt_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        txt_hdr.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(txt_hdr, text="Agendamento", font=("Segoe UI", 17, "bold"),
                    text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(txt_hdr, text="Cópia automática de agendamento", font=("Segoe UI", 12),
                    text_color=COR_DETALHE, anchor="w").pack(anchor="w")

        ctk.CTkButton(
            hdr, text=f"👤  CRIADO POR: {NOME_CRIADOR}", font=("Segoe UI", 9),
            fg_color="transparent", text_color=COR_MUTED, hover_color=COR_CARD,
            corner_radius=6, height=22, anchor="e",
            command=lambda: webbrowser.open(LINK_GITHUB_CRIADOR)
        ).pack(side="right", anchor="n")

        self.frm_controle = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frm_controle.pack(fill="both", expand=True, padx=24)

        self.frm_btn = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frm_btn.pack(fill="x", padx=24, pady=(12, 20))
        ctk.CTkButton(self.frm_btn, text="✖  Fechar", font=("Segoe UI", 11),
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                     corner_radius=8, height=36,
                     command=self._fechar).pack(side="right")

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

    def _ir_para_etapa(self, etapa):
        self._limpar_controle()
        getattr(self, f"_etapa_{etapa}")()

    def _mostrar_continuar(self, spoiler_texto, proxima_etapa, texto_botao="Continuar  →"):
        frm = ctk.CTkFrame(self.frm_controle, fg_color="transparent")
        frm.pack(fill="x", pady=(14, 0))
        if spoiler_texto:
            ctk.CTkLabel(frm, text=spoiler_texto, font=("Segoe UI", 10),
                        text_color=COR_MUTED, anchor="w").pack(anchor="w", pady=(0, 6))
        ctk.CTkButton(frm, text=texto_botao, font=("Segoe UI", 12, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=8, height=38,
                     command=lambda: self._ir_para_etapa(proxima_etapa)).pack(fill="x")


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA 0 -- início
    # ─── ⋆⋅☆⋅⋆ ───
    def _verificar_lock_inicial(self):
        time.sleep(0.3)
        pode_rodar, info_lock = _verificar_instancia_unica()
        if not pode_rodar:
            self.root.after(0, lambda: self._tela_bloqueado(info_lock))
            return
        self.root.after(0, lambda: self._ir_para_etapa("bibliotecas"))

    def _tela_bloqueado(self, info_lock):
        self._limpar_controle()
        card = self._card()
        ctk.CTkLabel(card, text="⚠️  ROBÔ JÁ ATIVO EM OUTRA MÁQUINA", font=("Segoe UI", 12, "bold"),
                    text_color=COR_AVISO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card, text=f"Em execução em: {info_lock}", font=("Segoe UI", 10),
                    text_color=COR_MUTED, anchor="w", wraplength=460,
                    justify="left").pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(card, text="Feche esta janela.", font=("Segoe UI", 10),
                    text_color=COR_MUTED, anchor="w").pack(anchor="w")


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA 1 -- bibliotecas
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_bibliotecas(self):
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
        threading.Thread(target=self._checar_bibliotecas, daemon=True).start()

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

    def _checar_bibliotecas(self):
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

        self._falha_lib = not _IMPORTS_OK
        self._status_geral("Tudo pronto!" if _IMPORTS_OK else "Há um problema a resolver.")
        self.root.after(500, self._mostrar_proximo_bibliotecas)

    def _mostrar_proximo_bibliotecas(self):
        if _IMPORTS_OK:
            self._mostrar_continuar("Próximo: verificar pastas de origem/destino", "pastas")
            return
        frm = ctk.CTkFrame(self.frm_controle, fg_color="transparent")
        frm.pack(fill="x", pady=(14, 0))
        ctk.CTkLabel(frm, text=f"❌  Erro: {_IMPORTS_ERRO[:150]}", font=("Segoe UI", 10),
                    text_color=COR_ERRO, wraplength=460, justify="left").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(frm, text="Algumas bibliotecas só funcionam de verdade depois "
                              "de reiniciar o programa.",
                    font=("Segoe UI", 9), text_color=COR_MUTED,
                    wraplength=460, justify="left").pack(anchor="w", pady=(0, 8))
        ctk.CTkButton(frm, text="🔄  Reiniciar", font=("Segoe UI", 11, "bold"),
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                     corner_radius=8, height=36,
                     command=self._reiniciar_programa).pack(fill="x")

    def _reiniciar_programa(self):
        try:
            subprocess.Popen([sys.executable, os.path.abspath(__file__)])
        except Exception as e:
            registrar_erro_permanente(f"REINICIAR -- {e}")
        finally:
            _liberar_lock()
            try:
                self.root.destroy()
            except Exception:
                pass
            os._exit(0)


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA 2 -- Pastas acessíveis?
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_pastas(self):
        card = self._card("Pastas")
        origem_ok  = os.path.isdir(ORIGEM_PASTA)
        destino_ok = os.path.isdir(DESTINO_PASTA)

        ctk.CTkLabel(card, text=("✅  Origem acessível" if origem_ok else "⚠️  Origem não encontrada agora"),
                    font=("Segoe UI", 11), text_color=(COR_OK if origem_ok else COR_AVISO),
                    anchor="w").pack(anchor="w")
        ctk.CTkLabel(card, text=ORIGEM_PASTA, font=("Segoe UI", 9), text_color=COR_MUTED,
                    anchor="w", wraplength=460, justify="left").pack(anchor="w")

        ctk.CTkLabel(card, text=("✅  Destino acessível" if destino_ok else "⚠️  Destino não encontrado agora"),
                    font=("Segoe UI", 11), text_color=(COR_OK if destino_ok else COR_AVISO),
                    anchor="w").pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(card, text=DESTINO_PASTA, font=("Segoe UI", 9), text_color=COR_MUTED,
                    anchor="w", wraplength=460, justify="left").pack(anchor="w")

        self._falha_pastas = not (origem_ok and destino_ok)
        if self._falha_pastas:
            ctk.CTkLabel(card, text="A rede pode estar temporariamente indisponível -- "
                                  "o robô continua tentando depois de iniciar.",
                        font=("Segoe UI", 9), text_color=COR_MUTED, anchor="w",
                        wraplength=460, justify="left").pack(anchor="w", pady=(10, 0))

        self._mostrar_continuar("Pronto para iniciar!", "final")


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA FINAL -- Iniciar
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_final(self):
        card = self._card()
        if self._falha_pastas:
            ctk.CTkLabel(card, text="⚠️  Uma das pastas não está acessível agora, mas você "
                                  "pode iniciar mesmo assim -- o robô vai continuar tentando.",
                        font=("Segoe UI", 11), text_color=COR_AVISO, anchor="w",
                        wraplength=460, justify="left").pack(anchor="w")
        else:
            ctk.CTkLabel(card, text="✅  Tudo certo! Pronto para iniciar.",
                        font=("Segoe UI", 13, "bold"), text_color=COR_OK, anchor="w").pack(anchor="w")

        ctk.CTkButton(self.frm_controle, text="▶  Iniciar", font=("Segoe UI", 12, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=8, height=38,
                     command=self._iniciar).pack(fill="x", pady=(6, 0))

    def _iniciar(self):
        self.aprovado = True
        self.root.destroy()

    def _fechar(self):
        self.aprovado = False
        _liberar_lock()
        self.root.destroy()


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# HISTÓRICO AO VIVO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_historico_aberto = False
MAX_BLOCOS_HISTORICO    = 200
TAMANHO_LEITURA_INICIAL = 300_000

class JanelaHistorico:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Agendamento -- Histórico")
        self.root.configure(fg_color=COR_FUNDO)
        self.root.resizable(False, False)
        self.root.geometry("580x680")
        self.root.protocol("WM_DELETE_WINDOW", self._fechar)

        self._parar       = threading.Event()
        self._pos_arquivo = 0

        self._construir_ui()
        self._carregar_inicial()
        threading.Thread(target=self._loop_tail, daemon=True).start()
        self.root.mainloop()

    def _construir_ui(self):
        hdr = ctk.CTkFrame(self.root, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(24, 12))
        badge = ctk.CTkLabel(hdr, text="📊", font=("Segoe UI", 20),
                             fg_color=COR_HEADER, text_color=COR_HEADER_TXT,
                             corner_radius=12, width=44, height=44)
        badge.pack(side="left")
        txt_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        txt_hdr.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(txt_hdr, text="Histórico ao vivo", font=("Segoe UI", 16, "bold"),
                    text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(txt_hdr, text="Agendamento", font=("Segoe UI", 11),
                    text_color=COR_DETALHE, anchor="w").pack(anchor="w")
        ctk.CTkLabel(hdr, text="●  ao vivo", font=("Segoe UI", 10),
                    text_color=COR_OK).pack(side="right", anchor="ne", pady=4)

        self.frm_log = ctk.CTkScrollableFrame(self.root, fg_color=COR_CARD, corner_radius=12,
                                              border_width=1, border_color=COR_BORDA)
        self.frm_log.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        rodape = ctk.CTkFrame(self.root, fg_color="transparent")
        rodape.pack(fill="x", padx=24, pady=(0, 20))
        ctk.CTkButton(rodape, text="📄  Abrir arquivo bruto (.txt)", font=("Segoe UI", 10),
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                     corner_radius=8, height=32,
                     command=lambda: os.startfile(LOG_ARQUIVO)).pack(side="left")
        ctk.CTkButton(rodape, text="✖  Fechar", font=("Segoe UI", 10),
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                     corner_radius=8, height=32,
                     command=self._fechar).pack(side="right")

    def _exibir_bloco(self, linhas):
        tag = _classificar_bloco(linhas)
        cabecalho, *resto = linhas
        _criar_linha_log(self.frm_log, cabecalho, tag)
        for l in resto:
            _criar_linha_log(self.frm_log, l, "detalhe")
        try:
            self.root.after(50, lambda: self.frm_log._parent_canvas.yview_moveto(1.0))
        except Exception:
            pass

    def _limpar_tela(self):
        for w in self.frm_log.winfo_children():
            w.destroy()

    def _carregar_inicial(self):
        try:
            with open(LOG_ARQUIVO, "rb") as f:
                f.seek(0, os.SEEK_END)
                tamanho = f.tell()
                ler = min(tamanho, TAMANHO_LEITURA_INICIAL)
                f.seek(tamanho - ler)
                bruto = f.read().decode("utf-8", errors="ignore")
                self._pos_arquivo = tamanho
        except Exception:
            bruto = ""
            self._pos_arquivo = 0

        blocos = _parsear_blocos_log(bruto)[-MAX_BLOCOS_HISTORICO:]
        if not blocos:
            _criar_linha_log(self.frm_log, "Sem registros ainda hoje.", "detalhe")
        for bloco in blocos:
            self._exibir_bloco(bloco)

    def _loop_tail(self):
        buffer_pendente = ""
        while not self._parar.is_set():
            try:
                tamanho_atual = os.path.getsize(LOG_ARQUIVO)
                if tamanho_atual < self._pos_arquivo:
                    self._pos_arquivo = 0
                    buffer_pendente = ""
                    self.root.after(0, self._limpar_tela)

                if tamanho_atual > self._pos_arquivo:
                    with open(LOG_ARQUIVO, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(self._pos_arquivo)
                        novo = f.read()
                    self._pos_arquivo = tamanho_atual
                    buffer_pendente += novo

                    sep = "-" * 60
                    partes = buffer_pendente.split(sep)
                    completos, buffer_pendente = partes[:-1], sep + partes[-1]
                    for pedaco in completos:
                        linhas = [l.rstrip() for l in pedaco.strip("\n").split("\n") if l.strip()]
                        if linhas:
                            self.root.after(0, lambda ls=linhas: self._exibir_bloco(ls))
            except Exception:
                pass
            time.sleep(2)

    def _fechar(self):
        global _historico_aberto
        self._parar.set()
        _historico_aberto = False
        try:
            self.root.destroy()
        except Exception:
            pass

def _abrir_historico_ao_vivo():
    global _historico_aberto
    if _historico_aberto:
        return
    _historico_aberto = True
    threading.Thread(target=_rodar_janela_historico, daemon=True).start()

def _rodar_janela_historico():
    global _historico_aberto
    try:
        JanelaHistorico()
    except Exception as e:
        registrar_erro_permanente(f"JANELA HISTÓRICO -- {e}")
    finally:
        _historico_aberto = False


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOOP PRINCIPAL
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _criar_icone_tray():
    try:
        from PIL import Image, ImageDraw
        img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, 63, 63],   fill="#18181B")
        draw.ellipse([16, 16, 47, 47], fill="#FFC72C")
        draw.ellipse([24, 24, 39, 39], fill="#18181B")
        return img
    except Exception:
        from PIL import Image
        return Image.new("RGBA", (64, 64), "#18181B")

def _esta_em_pausa(agora=None):
    agora = agora or datetime.now()
    hora_atual = agora.time()
    if HORA_ENCERRAR <= HORA_RETOMAR:
        return HORA_ENCERRAR <= hora_atual < HORA_RETOMAR
    return hora_atual >= HORA_ENCERRAR or hora_atual < HORA_RETOMAR

INTERVALO_DIAGNOSTICO = 3 * 60 * 60

def _diagnostico_periodico(ultima_modificacao_conhecida):
    caminho, msg = _resolver_origem_com_timeout()
    ok_mtime, mtime = (_com_timeout(os.path.getmtime, caminho) if caminho else (False, None))
    if caminho and ok_mtime:
        bate = mtime == ultima_modificacao_conhecida
        registrar_log([
            f"🔎  Checagem periódica (a cada {INTERVALO_DIAGNOSTICO // 3600}h, independente de mudança)",
            f"📅  {_agora_completo()}",
            f"📄  Mais recente na origem agora: {os.path.basename(caminho)}",
            f"🔁  Corresponde ao último arquivo processado: {'SIM' if bate else 'NÃO -- DIVERGENTE!'}",
        ])
        if not bate:
            registrar_erro_permanente(
                f"DIAGNÓSTICO PERIÓDICO -- origem tem arquivo mais recente "
                f"({os.path.basename(caminho)}) que o robô ainda não processou.")
    else:
        registrar_log([
            f"🔎  Checagem periódica (a cada {INTERVALO_DIAGNOSTICO // 3600}h, independente de mudança)",
            f"📅  {_agora_completo()}",
            msg or f"⏱️  Falha ao checar a data do arquivo (rede sem resposta): {mtime}",
        ])

def _loop_agendamento():
    while not _parar_loop.is_set():
        try:
            _loop_agendamento_interno()
            break
        except Exception as e:
            try:
                import traceback
                registrar_erro_permanente(f"LOOP MORREU SEM TRATAMENTO -- reiniciando automaticamente. {e}\n{traceback.format_exc()}")
                registrar_log([
                    "💥  O loop principal parou por um erro inesperado -- reiniciando automaticamente",
                    f"🕐  {_agora_completo()}",
                    f"     Detalhe: {e}",
                ])
            except Exception:
                pass
            for _ in range(30):
                if _parar_loop.is_set(): break
                time.sleep(1)
    _liberar_lock()

def _loop_agendamento_interno():
    global _status_atual

    _gerenciar_log()
    registrar_log([
        "🤖  AGENDAMENTO -- SISTEMA INICIADO",
        f"📅  Data: {_agora_completo()}",
        f"📁  Monitorando: {os.path.join(ORIGEM_PASTA, ORIGEM_PADRAO)}",
        f"📤  Destino:     {os.path.join(DESTINO_PASTA, NOME_DESTINO)}",
        f"PID: {os.getpid()} | PC: {os.environ.get('COMPUTERNAME','?')}",
        f"Pausa noturna: {HORA_ENCERRAR.strftime('%H:%M')} -- {HORA_RETOMAR.strftime('%H:%M')} (retomada automática)",
    ])
    _status_atual = "Ativo"

    caminho_inicial, msg_inicial = _resolver_origem_com_timeout()
    ultima_modificacao_conhecida = 0

    if caminho_inicial:
        ok_mtime, mtime_origem = _com_timeout(os.path.getmtime, caminho_inicial)
        if ok_mtime:
            destino_final = os.path.join(DESTINO_PASTA, NOME_DESTINO)

            precisa_sincronizar = False
            motivo = ""
            ok_existe, destino_existe = _com_timeout(os.path.exists, destino_final)
            if ok_existe and not destino_existe:
                precisa_sincronizar = True
                motivo = "Destino ainda não existe"
            elif ok_existe:
                ok_mtime_dest, mtime_destino = _com_timeout(os.path.getmtime, destino_final)
                if ok_mtime_dest and mtime_origem > mtime_destino:
                    precisa_sincronizar = True
                    motivo = "Origem mais recente que o destino atual"

            if precisa_sincronizar:
                linhas_sync = [
                    "🔄  Sincronizando ao iniciar",
                    f"📅  {_agora_completo()}",
                    f"📁  {motivo}",
                    f"📄  Arquivo: {os.path.basename(caminho_inicial)}",
                ]
                if msg_inicial:
                    linhas_sync.append(msg_inicial)
                registrar_log(linhas_sync)

                sucesso, msg_copia = _copiar_com_retry(caminho_inicial, DESTINO_PASTA)
                registrar_log([f"🕐  {_agora_completo()}", msg_copia])

            ultima_modificacao_conhecida = mtime_origem

    ultimo_heartbeat   = time.time()
    ultimo_diagnostico = time.time()
    estava_pausado     = False

    while not _parar_loop.is_set():
        agora    = datetime.now()
        em_pausa = _esta_em_pausa(agora)

        if em_pausa:
            if not estava_pausado:
                registrar_log([
                    f"PAUSA -- Encerramento automático às {HORA_ENCERRAR.strftime('%H:%M')}h.",
                    f"Data: {_agora_completo()}",
                    f"Retoma automaticamente às {HORA_RETOMAR.strftime('%H:%M')}h.",
                ])
                estava_pausado = True
            _status_atual = f"🌙 Pausado até {HORA_RETOMAR.strftime('%H:%M')}"

            if time.time() - ultimo_heartbeat >= INTERVALO_HEARTBEAT:
                _atualizar_heartbeat_lock()
                ultimo_heartbeat = time.time()

            for _ in range(30):
                if _parar_loop.is_set(): break
                time.sleep(1)
            continue

        if estava_pausado:
            registrar_log([
                f"RETOMANDO -- Operação normal retomada às {HORA_RETOMAR.strftime('%H:%M')}h.",
                f"Data: {_agora_completo()}",
            ])
            estava_pausado = False
            _status_atual = "Ativo"

            caminho_retomada, msg_retomada = _resolver_origem_com_timeout()
            if caminho_retomada:
                linhas_retomada = [
                    "🔄  Recopiando ao retomar (a pasta de destino pode ter sido limpa durante a pausa)",
                    f"📅  {_agora_completo()}",
                    f"📄  Arquivo: {os.path.basename(caminho_retomada)}",
                ]
                if msg_retomada:
                    linhas_retomada.append(msg_retomada)
                registrar_log(linhas_retomada)

                sucesso_retomada, msg_copia_retomada = _copiar_com_retry(caminho_retomada, DESTINO_PASTA)
                registrar_log([f"🕐  {_agora_completo()}", msg_copia_retomada])
                if sucesso_retomada:
                    ok_mtime_retomada, mtime_retomada = _com_timeout(os.path.getmtime, caminho_retomada)
                    if ok_mtime_retomada:
                        ultima_modificacao_conhecida = mtime_retomada
            else:
                registrar_log([f"🕐  {_agora_completo()}", msg_retomada])

        try:
            caminho_origem, msg_resolucao = _resolver_origem_com_timeout()

            if caminho_origem is None:
                registrar_log([f"🕐  {_agora_completo()}", msg_resolucao])
                if msg_resolucao and "⏱️" in msg_resolucao:
                    registrar_erro_permanente(f"TIMEOUT PASTA DE REDE -- {msg_resolucao}")
            else:
                ok_mtime_ciclo, modificacao_atual = _com_timeout(os.path.getmtime, caminho_origem)

                if not ok_mtime_ciclo:
                    registrar_log([f"🕐  {_agora_completo()}",
                                   f"⏱️  Falha ao checar a data do arquivo (rede sem resposta): {modificacao_atual}"])
                    registrar_erro_permanente(f"TIMEOUT GETMTIME -- {modificacao_atual}")

                elif modificacao_atual != ultima_modificacao_conhecida:
                    linhas_alteracao = [
                        "👀  Alteração detectada",
                        f"📅  {_agora_completo()}",
                        f"📁  Arquivo: {os.path.basename(caminho_origem)}",
                    ]
                    if msg_resolucao:
                        linhas_alteracao.append(msg_resolucao)
                    linhas_alteracao.append(f"⏳  Aguardando {MINUTOS_ESPERA} min antes de copiar...")
                    registrar_log(linhas_alteracao)
                    _status_atual = f"Aguardando cópia -- {agora.strftime('%H:%M')}"

                    for _ in range(MINUTOS_ESPERA * 60):
                        if _parar_loop.is_set(): break
                        time.sleep(1)

                    if not _parar_loop.is_set():
                        sucesso, msg_copia = _copiar_com_retry(caminho_origem, DESTINO_PASTA)
                        if sucesso:
                            ultima_modificacao_conhecida = modificacao_atual
                            _status_atual = f"OK -- {datetime.now().strftime('%H:%M')}"
                        else:
                            _status_atual = f"Erro -- {datetime.now().strftime('%H:%M')}"
                        registrar_log([f"🕐  {_agora_completo()}", msg_copia])

        except Exception as e:
            _status_atual = f"Erro -- {datetime.now().strftime('%H:%M')}"
            registrar_log([
                "💥  Erro crítico no loop principal",
                f"🕐  {_agora_completo()}",
                f"     Detalhe: {e}",
            ])
            registrar_erro_permanente(f"LOOP -- {e}")

        if time.time() - ultimo_heartbeat >= INTERVALO_HEARTBEAT:
            _atualizar_heartbeat_lock()
            ultimo_heartbeat = time.time()

        if time.time() - ultimo_diagnostico >= INTERVALO_DIAGNOSTICO:
            _diagnostico_periodico(ultima_modificacao_conhecida)
            ultimo_diagnostico = time.time()

        for _ in range(INTERVALO_CHECK):
            if _parar_loop.is_set(): break
            time.sleep(1)

def _iniciar_tray():
    try:
        import pystray
    except ImportError:
        _loop_agendamento()
        return

    def texto_status(item):
        return f"Status: {_status_atual}"

    def parar(icon, item):
        _parar_loop.set()
        _liberar_lock()
        registrar_log(["Robô parado pelo usuário.", f"Data: {_agora_completo()}"])
        threading.Timer(5, os._exit, args=(0,)).start()
        icon.stop()

    def abrir_historico(icon, item):
        _abrir_historico_ao_vivo()

    menu = pystray.Menu(
        pystray.MenuItem("📊  Ver histórico", abrir_historico, default=True),
        pystray.MenuItem(texto_status, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("⏹  Parar robô", parar),
    )
    icone = pystray.Icon("Agendamento", _criar_icone_tray(), "Agendamento", menu=menu)

    threading.Thread(target=_loop_agendamento, daemon=True).start()
    icone.run()


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# PONTO DE ENTRADA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
if __name__ == "__main__":
    try:
        janela = JanelaLancamento()
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
                "Agendamento -- Erro ao iniciar",
                f"O robô encontrou um erro e não conseguiu abrir:\n\n{_e}\n\n"
                f"Detalhes salvos em: erro_fatal.txt (nesta mesma pasta)."
            )
            _raiz_erro.destroy()
        except Exception:
            pass
        sys.exit(1)

    if not janela.aprovado:
        sys.exit(0)
    _iniciar_tray()
