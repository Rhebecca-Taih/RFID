# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# BIBLIOTECAS
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
import os
import sys
import time
import glob
import shutil
import subprocess
import threading
import importlib
import webbrowser
from datetime import datetime

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
    _splash.title("Robô Controle KPI OneDrive")
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


USUARIO_WINDOWS = os.environ.get("USERNAME", "")


PASTA_ONEDRIVE_BASE = os.getenv("PASTA_ONEDRIVE_BASE", "")

INTERVALO_CHECK  = int(os.getenv("INTERVALO_CHECK_SEGUNDOS", "3600"))
SEGUNDOS_ESPERA  = int(os.getenv("SEGUNDOS_ESPERA", "20"))
MAX_TENTATIVAS   = int(os.getenv("MAX_TENTATIVAS", "3"))

INTERVALO_HEARTBEAT = 10 * 60
EXPIRACAO_LOCK       = 2 * 60 * 60

def _carregar_tarefas():
    tarefas = []
    n = 1
    while True:
        origem = os.getenv(f"TAREFA_{n}_ORIGEM")
        if not origem:
            break
        subpasta = os.getenv(f"TAREFA_{n}_DESTINO_SUBPASTA", "")
        nome     = os.getenv(f"TAREFA_{n}_NOME", os.path.basename(origem))


        link_sharepoint = os.getenv(f"TAREFA_{n}_LINK_SHAREPOINT", "")
        destino_pasta = os.path.join("C:\\Users", USUARIO_WINDOWS, PASTA_ONEDRIVE_BASE, subpasta)
        tarefas.append({
            "id": n,
            "origem": origem,
            "destino_pasta": destino_pasta,
            "destino_nome": nome,
            "link_sharepoint": link_sharepoint,
            "ultima_modificacao_conhecida": 0,
            "ultimo_tamanho_conhecido": -1,
        })
        n += 1
    return tarefas


# Crédito > aparece no canto superior direito do cabeçalho.
NOME_CRIADOR        = os.getenv("NOME_CRIADOR",        "Rhebecca-Taih")
LINK_GITHUB_CRIADOR = os.getenv("LINK_GITHUB_CRIADOR", "https://github.com/Rhebecca-Taih")

_status_atual        = "Aguardando..."
_parar_loop          = threading.Event()
_forcar_sincronizacao = threading.Event()


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
COR_BTN_B        = "#3D8BFF"
COR_BTN_B_TXT    = "#FFFFFF"
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

LOG_ARQUIVO          = os.path.join(_pasta_logs,    "historico_kpi_onedrive.txt")
LOG_ERROS_PERMANENTE = os.path.join(_pasta_logs,    "historico_erros.txt")
LOCK_ARQUIVO         = os.path.join(_pasta_runtime, "controle_kpi_onedrive.lock")


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

PASTA_LOG_LOCAL = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "RobosBureau", "Controle KPI OneDrive")
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

def _ultimo_status_log():
    if not os.path.exists(LOG_ARQUIVO):
        return "Sem registros anteriores."
    try:
        with open(LOG_ARQUIVO, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f.readlines()
                      if l.strip() and not l.strip().startswith("-")
                      and not l.strip().startswith("=")
                      and "LOG DE AUTOMACAO" not in l]
        for linha in reversed(linhas):
            if any(e in linha for e in ["✅", "❌", "🤖", "👀", "🕐", "🚨"]):
                return linha
        return linhas[-1] if linhas else "Sem registros."
    except Exception:
        return "Erro ao ler o log."


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
    if any(e in texto for e in ["❌", "🚨", "ERRO", "FALHA", "CRITICO"]):
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
# ONEDRIVE
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# Falha na checagem conta como rodando > evita alarme falso do tasklist.
def _onedrive_rodando():
    try:
        r = subprocess.run('tasklist /FI "IMAGENAME eq OneDrive.exe" /NH',
                           shell=True, capture_output=True, text=True,
                           creationflags=_NO_WINDOW)
        return "OneDrive.exe" in r.stdout
    except Exception:
        return True

def _onedrive_esta_logado():
    try:
        import winreg
        for tipo_conta in ("Business1", "Personal"):
            try:
                chave = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    f"Software\\Microsoft\\OneDrive\\Accounts\\{tipo_conta}"
                )
                email, _ = winreg.QueryValueEx(chave, "UserEmail")
                winreg.CloseKey(chave)
                if email:
                    return True, email
            except FileNotFoundError:
                continue
            except Exception:
                continue
        return False, ""
    except Exception:
        return True, ""

def _tentar_reabrir_onedrive():
    caminho_onedrive = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "OneDrive", "OneDrive.exe")
    try:
        if os.path.exists(caminho_onedrive):
            subprocess.Popen([caminho_onedrive, "/background"], creationflags=_NO_WINDOW)
            return True
    except Exception:
        pass
    return False

def _checar_arquivos_conflito(destino_pasta, nome_canonico):
    stem, ext = os.path.splitext(nome_canonico)
    padrao = os.path.join(destino_pasta, f"{stem}*{ext}")
    try:
        encontrados = glob.glob(padrao)
    except Exception:
        return []
    canonico_lower = nome_canonico.lower()
    return [f for f in encontrados if os.path.basename(f).lower() != canonico_lower]

def _pos_copia_diagnostico(destino_pasta, destino_nome):
    destino_final = os.path.join(destino_pasta, destino_nome)
    linhas = []

    if not _onedrive_rodando():
        linhas.append("🚨  OneDrive não está em execução nesta máquina -- o arquivo foi copiado LOCALMENTE, mas não vai subir para a nuvem enquanto o OneDrive não for reaberto.")
        if _tentar_reabrir_onedrive():
            linhas.append("🔄  Reabertura automática do OneDrive solicitada.")
        else:
            linhas.append("⚠️  OneDrive não localizado no caminho padrão -- abrir manualmente.")
        registrar_erro_permanente(f"ONEDRIVE INATIVO -- {destino_final} copiado localmente, upload não garantido")

    logado_ok, _ = _onedrive_esta_logado()
    if not logado_ok:
        linhas.append("🚨  Nenhuma conta vinculada ao OneDrive nesta máquina -- o arquivo foi copiado LOCALMENTE, mas não vai subir para nuvem até alguém logar (a autenticação exige verificação adicional, não dá para automatizar).")
        registrar_erro_permanente(f"ONEDRIVE SEM CONTA LOGADA -- {destino_final} copiado localmente, upload não garantido")

    conflitos = _checar_arquivos_conflito(destino_pasta, destino_nome)
    if conflitos:
        linhas.append(f"⚠️  {len(conflitos)} arquivo(s) parecido(s) com '{destino_nome}' na pasta de destino -- pode ser um conflito de sincronização do OneDrive:")
        for c in conflitos:
            linhas.append(f"     {os.path.basename(c)}")
        registrar_erro_permanente(f"POSSÍVEL CONFLITO ONEDRIVE -- {destino_final} -- {[os.path.basename(c) for c in conflitos]}")

    if linhas:
        registrar_log(linhas)


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# CÓPIA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _copiar_com_retry(origem, destino_pasta, destino_nome):
    destino_final = os.path.join(destino_pasta, destino_nome)

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            if not os.path.isdir(destino_pasta):
                return False, f"❌  Pasta de destino não encontrada: {destino_pasta}"

            shutil.copy2(origem, destino_final)

            tam_origem  = os.path.getsize(origem)
            tam_destino = os.path.getsize(destino_final)

            if tam_origem != tam_destino:
                msg = (f"⚠️  Cópia incompleta (tentativa {tentativa}/{MAX_TENTATIVAS}).\n"
                       f"     Origem:  {_tamanho_formatado(origem)}\n"
                       f"     Destino: {_tamanho_formatado(destino_final)}")
                if tentativa < MAX_TENTATIVAS:
                    time.sleep(5)
                    continue
                return False, msg

            msg = (f"✅  Copiado com sucesso.\n"
                   f"     Tamanho:  {_tamanho_formatado(destino_final)}\n"
                   f"     Destino:  {destino_final}")
            return True, msg

        except PermissionError:
            if tentativa < MAX_TENTATIVAS:
                time.sleep(30)
            else:
                return False, f"🔒  Arquivo permaneceu em uso após {MAX_TENTATIVAS} tentativas. Abortando."

        except Exception as e:
            if tentativa < MAX_TENTATIVAS:
                time.sleep(5)
            else:
                return False, f"❌  Erro inesperado após {MAX_TENTATIVAS} tentativas: {type(e).__name__}: {e}"

    return False, f"❌  Falha após {MAX_TENTATIVAS} tentativas."


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# JANELA DE LANÇAMENTO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
class JanelaLancamento:
    def __init__(self):
        self.aprovado      = False
        self._falha_lib    = False
        self._falha_pastas = False
        self._tarefas       = _carregar_tarefas()

        self.root = ctk.CTk()
        self.root.title("Robô Controle KPI OneDrive")
        self.root.configure(fg_color=COR_FUNDO)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._fechar)

        self._construir_ui()
        self._centralizar(600, 660)
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

        badge = ctk.CTkLabel(hdr, text="☁️", font=("Segoe UI", 20),
                             fg_color=COR_HEADER, text_color=COR_HEADER_TXT,
                             corner_radius=12, width=44, height=44)
        badge.pack(side="left")

        txt_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        txt_hdr.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(txt_hdr, text="Robô Controle KPI OneDrive", font=("Segoe UI", 17, "bold"),
                    text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(txt_hdr, text="Sincroniza indicadores com o OneDrive", font=("Segoe UI", 12),
                    text_color=COR_DETALHE, anchor="w").pack(anchor="w")

        ctk.CTkButton(
            hdr, text=f"👤  CRIADO POR: {NOME_CRIADOR}", font=("Segoe UI", 9),
            fg_color="transparent", text_color=COR_MUTED, hover_color=COR_CARD,
            corner_radius=6, height=22, anchor="e",
            command=lambda: webbrowser.open(LINK_GITHUB_CRIADOR)
        ).pack(side="right", anchor="n")


        self.frm_controle = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
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
        ctk.CTkLabel(card, text="⚠️  ROBÔ JÁ ATIVO NESTA MÁQUINA", font=("Segoe UI", 12, "bold"),
                    text_color=COR_AVISO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card, text=f"Em execução {info_lock}", font=("Segoe UI", 10),
                    text_color=COR_MUTED, anchor="w", wraplength=520,
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
                registrar_erro_permanente(f"INSTALAR {nome_pip} -- {type(e_lib).__name__}: {e_lib}")
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
            self._mostrar_continuar("Próximo: verificar tarefas e OneDrive", "pastas")
            return
        frm = ctk.CTkFrame(self.frm_controle, fg_color="transparent")
        frm.pack(fill="x", pady=(14, 0))
        ctk.CTkLabel(frm, text=f"❌  Erro: {_IMPORTS_ERRO[:150]}", font=("Segoe UI", 10),
                    text_color=COR_ERRO, wraplength=520, justify="left").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(frm, text="Algumas bibliotecas só funcionam de verdade depois "
                              "de reiniciar o programa.",
                    font=("Segoe UI", 9), text_color=COR_MUTED,
                    wraplength=520, justify="left").pack(anchor="w", pady=(0, 8))
        ctk.CTkButton(frm, text="🔄  Reiniciar", font=("Segoe UI", 11, "bold"),
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                     corner_radius=8, height=36,
                     command=self._reiniciar_programa).pack(fill="x")

    def _reiniciar_programa(self):
        try:
            subprocess.Popen([sys.executable, os.path.abspath(__file__)])
        except Exception as e:
            registrar_erro_permanente(f"REINICIAR -- {type(e).__name__}: {e}")
        finally:
            _liberar_lock()
            try:
                self.root.destroy()
            except Exception:
                pass
            os._exit(0)


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA 2 -- pastas
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_pastas(self):
        card = self._card(f"Tarefas ({len(self._tarefas)}) -- usuário: {USUARIO_WINDOWS}")

        if not self._tarefas:
            ctk.CTkLabel(card, text="🚨  Nenhuma tarefa configurada no .env "
                                  "(TAREFA_1_ORIGEM em diante).",
                        font=("Segoe UI", 11), text_color=COR_ERRO, anchor="w",
                        wraplength=520, justify="left").pack(anchor="w")
            self._falha_pastas = True
            self._mostrar_continuar("⛔  Configure ao menos uma tarefa e clique em Verificar novamente.",
                                    "pastas", texto_botao="🔄  Verificar novamente")
            return

        bloqueio = False
        for t in self._tarefas:
            origem_ok = os.path.exists(t["origem"])
            destino_ok = os.path.isdir(t["destino_pasta"])
            if not (origem_ok and destino_ok):
                bloqueio = True

            ctk.CTkLabel(card, text=f"Tarefa {t['id']}: {t['destino_nome']}", font=("Segoe UI", 11, "bold"),
                        text_color=COR_TEXTO, anchor="w").pack(anchor="w", pady=(8, 2))
            ctk.CTkLabel(card, text=("✅  Origem acessível" if origem_ok else "🚨  Origem não encontrada"),
                        font=("Segoe UI", 10), text_color=(COR_OK if origem_ok else COR_ERRO),
                        anchor="w").pack(anchor="w")
            ctk.CTkLabel(card, text=t["origem"], font=("Segoe UI", 9), text_color=COR_MUTED,
                        anchor="w", wraplength=520, justify="left").pack(anchor="w")
            ctk.CTkLabel(card, text=("✅  Destino acessível" if destino_ok else "🚨  Destino não encontrado"),
                        font=("Segoe UI", 10), text_color=(COR_OK if destino_ok else COR_ERRO),
                        anchor="w").pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(card, text=t["destino_pasta"], font=("Segoe UI", 9), text_color=COR_MUTED,
                        anchor="w", wraplength=520, justify="left").pack(anchor="w")
            if not destino_ok and t.get("link_sharepoint"):


                ctk.CTkButton(
                    card, text="🔗  Abrir biblioteca no SharePoint e sincronizar",
                    font=("Segoe UI", 9, "underline"), fg_color="transparent",
                    text_color=COR_BTN_B, hover_color=COR_CARD, anchor="w",
                    height=20, corner_radius=4,
                    command=lambda link=t["link_sharepoint"]: webbrowser.open(link)
                ).pack(anchor="w", pady=(2, 0))

        onedrive_ok = _onedrive_rodando()
        ctk.CTkLabel(card, text=("✅  OneDrive em execução" if onedrive_ok else "🚨  OneDrive NÃO está em execução"),
                    font=("Segoe UI", 11), text_color=(COR_OK if onedrive_ok else COR_ERRO),
                    anchor="w").pack(anchor="w", pady=(12, 0))
        if not onedrive_ok:
            bloqueio = True
            ctk.CTkLabel(card, text="Sem o OneDrive aberto, nada sobe para nuvem. Abra o OneDrive e "
                                  "clique em \"Verificar novamente\".",
                        font=("Segoe UI", 9), text_color=COR_MUTED, anchor="w",
                        wraplength=520, justify="left").pack(anchor="w")

        logado_ok, email_logado = _onedrive_esta_logado()
        ctk.CTkLabel(card, text=(f"✅  OneDrive logado ({email_logado})" if logado_ok else "🚨  Nenhuma conta vinculada ao OneDrive"),
                    font=("Segoe UI", 11), text_color=(COR_OK if logado_ok else COR_ERRO),
                    anchor="w").pack(anchor="w", pady=(6, 0))
        if not logado_ok:
            bloqueio = True
            ctk.CTkLabel(card, text="Sem conta logada, nada sobe para nuvem -- e o login exige verificação "
                                  "adicional (MFA), que precisa ser feita por uma pessoa. Abra o OneDrive, "
                                  "faça login e clique em \"Verificar novamente\".",
                        font=("Segoe UI", 9), text_color=COR_MUTED, anchor="w",
                        wraplength=520, justify="left").pack(anchor="w")


        self._falha_pastas = bloqueio
        if bloqueio:
            ctk.CTkLabel(card, text="⛔  Corrija o que está marcado acima antes de continuar.",
                        font=("Segoe UI", 10, "bold"), text_color=COR_ERRO, anchor="w",
                        wraplength=520, justify="left").pack(anchor="w", pady=(10, 0))
            self._mostrar_continuar("", "pastas", texto_botao="🔄  Verificar novamente")
            return

        self._mostrar_continuar("Pronto para iniciar!", "final")


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA FINAL
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_final(self):


        card = self._card()
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
        self.root.title("Robô Controle KPI OneDrive -- Histórico")
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
        ctk.CTkLabel(txt_hdr, text="Robô Controle KPI OneDrive", font=("Segoe UI", 11),
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
        registrar_erro_permanente(f"JANELA HISTÓRICO -- {type(e).__name__}: {e}")
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

def _sincronizar_tarefa_se_precisar(t, motivo_forcado=None):
    if not os.path.exists(t["origem"]):
        registrar_log([f"🕐  {_agora_completo()}", f"⚠️  Tarefa {t['id']}: origem não encontrada agora.", f"     {t['origem']}"])
        return

    mtime_atual = os.path.getmtime(t["origem"])
    tam_atual   = os.path.getsize(t["origem"])
    mudou = mtime_atual != t["ultima_modificacao_conhecida"] or tam_atual != t["ultimo_tamanho_conhecido"]

    if not (mudou or motivo_forcado):
        return

    if motivo_forcado:
        registrar_log([f"🔄  Tarefa {t['id']}: sincronizando ao iniciar", f"📅  {_agora_completo()}", f"📁  {motivo_forcado}"])
    else:
        registrar_log([
            f"👀  Tarefa {t['id']}: alteração detectada na origem",
            f"📅  {_agora_completo()}",
            f"⏳  Aguardando {SEGUNDOS_ESPERA}s antes de copiar...",
        ])
        for _ in range(SEGUNDOS_ESPERA):
            if _parar_loop.is_set(): return
            time.sleep(1)

    sucesso, msg_copia = _copiar_com_retry(t["origem"], t["destino_pasta"], t["destino_nome"])
    registrar_log([f"🕐  {_agora_completo()}", msg_copia])
    if sucesso:
        t["ultima_modificacao_conhecida"] = mtime_atual
        t["ultimo_tamanho_conhecido"] = tam_atual
        _pos_copia_diagnostico(t["destino_pasta"], t["destino_nome"])

def _loop_vigia_interno():
    global _status_atual

    _gerenciar_log()
    tarefas = _carregar_tarefas()

    if not tarefas:
        registrar_log(["❌  Nenhuma tarefa configurada -- confira TAREFA_1_ORIGEM em diante no .env."])
        _status_atual = "Sem tarefas configuradas"
        return

    linhas_inicio = [
        "🤖  ROBÔ CONTROLE KPI ONEDRIVE -- SISTEMA INICIADO",
        f"📅  Data: {_agora_completo()}",
        f"PID: {os.getpid()} | PC: {os.environ.get('COMPUTERNAME','?')} | Usuário: {USUARIO_WINDOWS}",
    ]
    for t in tarefas:
        destino_final = os.path.join(t["destino_pasta"], t["destino_nome"])
        linhas_inicio.append(f"📁  Tarefa {t['id']}: {t['origem']}  →  {destino_final}")
    registrar_log(linhas_inicio)
    _status_atual = "Ativo"

    # Primeira passada copia tudo > o destino começa atualizado; depois, só copia quando há mudança.
    for t in tarefas:
        destino_final = os.path.join(t["destino_pasta"], t["destino_nome"])
        if not os.path.exists(t["origem"]):
            continue
        try:
            mtime_origem = os.path.getmtime(t["origem"])
            tam_origem   = os.path.getsize(t["origem"])
            motivo = None
            if not os.path.exists(destino_final):
                motivo = "Destino ainda não existe"
            else:
                try:
                    if mtime_origem > os.path.getmtime(destino_final) or tam_origem != os.path.getsize(destino_final):
                        motivo = "Origem diferente do destino atual"
                except Exception:
                    pass
            t["ultima_modificacao_conhecida"] = mtime_origem
            t["ultimo_tamanho_conhecido"] = tam_origem
            if motivo:


                _sincronizar_tarefa_se_precisar(t, motivo_forcado=motivo)
        except Exception:
            pass

    ultimo_heartbeat = time.time()

    while not _parar_loop.is_set():
        for t in tarefas:
            try:
                _sincronizar_tarefa_se_precisar(t)
            except Exception as e:
                registrar_log([
                    f"💥  Erro crítico na tarefa {t['id']}",
                    f"🕐  {_agora_completo()}",
                    f"     Detalhe: {type(e).__name__}: {e}",
                ])
                registrar_erro_permanente(f"TAREFA {t['id']} -- {type(e).__name__}: {e}")
            if _parar_loop.is_set():
                break

        _status_atual = f"OK -- {datetime.now().strftime('%H:%M')}"


        for _ in range(INTERVALO_CHECK):
            if _parar_loop.is_set() or _forcar_sincronizacao.is_set():
                break
            if time.time() - ultimo_heartbeat >= INTERVALO_HEARTBEAT:
                _atualizar_heartbeat_lock()
                ultimo_heartbeat = time.time()
            time.sleep(1)
        if _forcar_sincronizacao.is_set():
            registrar_log(["🔄  Sincronização manual acionada pela bandeja -- checando todas as tarefas agora."])
            _forcar_sincronizacao.clear()

def _loop_vigia():
    while not _parar_loop.is_set():
        try:
            _loop_vigia_interno()
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

def _iniciar_tray():
    try:
        import pystray
    except ImportError:
        _loop_vigia()
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

    def sincronizar_agora(icon, item):
        _forcar_sincronizacao.set()

    menu = pystray.Menu(
        pystray.MenuItem("📊  Ver histórico", abrir_historico, default=True),
        pystray.MenuItem(texto_status, None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("🔄  Sincronizar agora", sincronizar_agora),
        pystray.MenuItem("⏹  Parar robô", parar),
    )
    icone = pystray.Icon("ControleKpiOneDrive", _criar_icone_tray(), "Robô Controle KPI OneDrive", menu=menu)

    threading.Thread(target=_loop_vigia, daemon=True).start()
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
                "Robô Controle KPI OneDrive -- Erro ao iniciar",
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
