# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# BIBLIOTECAS
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
import os
import re
import csv
import sys
import glob
import json
import time
import shutil
import subprocess
import threading
import importlib
import webbrowser
from datetime import datetime, timedelta

import tkinter as tk

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pasta_script = os.path.dirname(os.path.abspath(__file__))
pasta_raiz   = os.path.dirname(pasta_script)
_NO_WINDOW   = getattr(subprocess, "CREATE_NO_WINDOW", 0)


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# DETECÇÃO PARA AUTO-INSTALAÇÃO DE BIBLIOTECAS
# Instalação ao vivo em _checar_ambiente (tela Bibliotecas).
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_LIBS = [
    ("openpyxl",      "openpyxl"),
    ("dotenv",        "python-dotenv"),
    ("selenium",      "selenium"),
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
    _splash.title("Robô de Impressão")
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
    global ctk, load_dotenv, openpyxl, load_workbook, Workbook, Calendar
    global webdriver, Options, Service, By, WebDriverWait, EC, Keys, TimeoutException, WebDriverException
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
        import openpyxl
        from openpyxl import load_workbook, Workbook
        from tkcalendar import Calendar
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.keys import Keys
        from selenium.common.exceptions import TimeoutException, WebDriverException
        _IMPORTS_OK = True
        _IMPORTS_ERRO = ""
    except Exception as _ex:
        _IMPORTS_OK = False
        _IMPORTS_ERRO = str(_ex)

_tentar_importar_reais()


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# CONFIGURAÇÕES
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
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

PORTAL_USER      = os.getenv("PORTAL_USER", "")
PORTAL_SENHA     = os.getenv("PORTAL_SENHA", "")
PORTAL_URL_LOGIN = os.getenv("PORTAL_URL_LOGIN", "")
PORTAL_SITE      = os.getenv("PORTAL_SITE", "")
CAMINHO_REDE_BIN = os.getenv("CAMINHO_REDE_BIN", "")

SETORES_DISPONIVEIS = [
    s.strip() for s in
    os.getenv("SETORES_PREPARADOR", "ELETRO-ELETRONICOS,BELEZA").split(",")
    if s.strip()
]


MODELO_DETECCAO_AUTOMATICA = "DETECÇÃO AUTOMÁTICA"
MODELOS_DISPONIVEIS = [MODELO_DETECCAO_AUTOMATICA] + [
    s.strip() for s in
    os.getenv("MODELOS_ETIQUETA_IMPRESSAO", "72x17 Eletro,46x8 Beleza,64x7 Beleza,44x19,44x19 Beleza").split(",")
    if s.strip()
]


_MAPA_MODELO_AUTOMATICO = {
    "72X17": "72x17 Eletro",
    "64X7":  "64x7 Beleza",
    "46X8":  "46x8 Beleza",
}

def _resolver_modelo_automatico(dados):
    modelo_curto = str(dados.get("VALIDAÇÃO MODELO", "") or "").strip().upper()
    return _MAPA_MODELO_AUTOMATICO.get(modelo_curto)
IMPRESSORAS_DISPONIVEIS = [
    s.strip() for s in
    os.getenv("IMPRESSORAS_DISPONIVEIS", "SATO 1,SATO 2,SATO 3,SATO PLUS METAL").split(",")
    if s.strip()
]


CAMINHO_REDE_BASE_GERAL  = os.getenv("CAMINHO_REDE_BASE_GERAL", "")
PASTA_BASE_GERAL_LOCAL   = os.path.join(pasta_script, "Base Geral")
CAMINHO_BASE_GERAL_LOCAL = os.path.join(PASTA_BASE_GERAL_LOCAL, "BASE GERAL.xlsx")
ABAS_BASE_GERAL          = ["PEDIDOS AGENDADOS"]
DIAS_CONSIDERAR_RECENTE  = 7

def _copiar_base_geral_local():
    try:
        if not os.path.exists(CAMINHO_REDE_BASE_GERAL):
            return False, f"BASE GERAL não encontrada na rede: {CAMINHO_REDE_BASE_GERAL}"
        os.makedirs(PASTA_BASE_GERAL_LOCAL, exist_ok=True)
        shutil.copy2(CAMINHO_REDE_BASE_GERAL, CAMINHO_BASE_GERAL_LOCAL)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# BASE GERAL (LOCAL)
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _chave_pedido(valor):
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    return _normalizar_zeros(str(valor if valor is not None else "").strip())

def _para_datetime(valor):
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, (int, float)) and not isinstance(valor, bool) and valor > 0:
        try:
            # 1899-12-30 é a época (dia 0) do sistema de data serial do Excel.
            return datetime(1899, 12, 30) + timedelta(days=float(valor))
        except Exception:
            return None
    return None

def _ler_base_geral_pedidos():
    if not os.path.exists(CAMINHO_BASE_GERAL_LOCAL):
        return None
    try:
        wb = load_workbook(CAMINHO_BASE_GERAL_LOCAL, data_only=True, read_only=True)
    except Exception as e:
        registrar_log([f"⚠️  Falha ao abrir a cópia local da BASE GERAL: {type(e).__name__}: {e}"])
        return None
    resultado = {}
    abas_lidas = 0
    try:
        for nome_aba in ABAS_BASE_GERAL:
            if nome_aba not in wb.sheetnames:
                continue
            ws = wb[nome_aba]
            try:
                primeira_linha = next(ws.iter_rows(min_row=1, max_row=1))
            except StopIteration:
                continue
            cabecalho = [str(c.value).strip().upper() if c.value is not None else "" for c in primeira_linha]
            if "PEDIDO" not in cabecalho:
                continue
            abas_lidas += 1
            idx_pedido   = cabecalho.index("PEDIDO")
            idx_data     = cabecalho.index("DATA") if "DATA" in cabecalho else None
            idx_impresso = cabecalho.index("IMPRESSO") if "IMPRESSO" in cabecalho else None
            for row in ws.iter_rows(min_row=2, values_only=True):
                if len(row) <= idx_pedido:
                    continue
                pedido_val = _chave_pedido(row[idx_pedido])
                if not pedido_val:
                    continue
                resultado.setdefault(pedido_val, None)
                if idx_data is None or idx_impresso is None or len(row) <= max(idx_data, idx_impresso):
                    continue
                impresso_val = row[idx_impresso]


                texto_impresso = str(impresso_val).strip().upper() if impresso_val is not None else ""
                if not texto_impresso or texto_impresso in ("FORA CDA", "MOV"):
                    continue
                data_dt = _para_datetime(row[idx_data])
                if data_dt and (resultado[pedido_val] is None or data_dt > resultado[pedido_val]):
                    resultado[pedido_val] = data_dt
    finally:
        wb.close()
    return resultado if abas_lidas else None

def _normalizar_zeros(valor):
    texto = str(valor or "").strip()
    sem_zeros = texto.lstrip("0")
    return sem_zeros if sem_zeros else ("0" if texto else "")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# COLMEIA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
LINK_COLMEIA_ARTIGOS = os.getenv("LINK_COLMEIA_ARTIGOS", "")
PASTA_COLMEIA_LOCAL  = os.path.join(pasta_script, "Colmeia")

def _baixar_colmeia_aba(nome_aba):
    if not LINK_COLMEIA_ARTIGOS:
        return None, "LINK_COLMEIA_ARTIGOS não configurado no .env"
    try:
        os.makedirs(PASTA_COLMEIA_LOCAL, exist_ok=True)
        padrao_arquivo = os.path.join(PASTA_COLMEIA_LOCAL, f"*{nome_aba}*.csv")
        for antigo in glob.glob(padrao_arquivo):
            try:
                os.remove(antigo)
            except Exception:
                pass

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1400,1000")
        options.binary_location = CHROME_PATH
        options.add_experimental_option("prefs", {
            "download.default_directory": PASTA_COLMEIA_LOCAL,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
        })
        svc = Service(executable_path=DRIVER_PATH)
        driver_colmeia = webdriver.Chrome(service=svc, options=options)
        driver_colmeia.set_page_load_timeout(60)
        try:
            driver_colmeia.execute_cdp_cmd("Page.setDownloadBehavior",
                                            {"behavior": "allow", "downloadPath": PASTA_COLMEIA_LOCAL})
            driver_colmeia.get(LINK_COLMEIA_ARTIGOS)
            time.sleep(10)
            iframe = driver_colmeia.find_element(By.ID, "WacFrame_Excel_0")
            driver_colmeia.switch_to.frame(iframe)
            time.sleep(2)

            abas = driver_colmeia.find_elements(By.XPATH, f"//*[normalize-space(text())='{nome_aba}']")
            if not abas:
                return None, f"Aba '{nome_aba}' não encontrada na planilha"
            driver_colmeia.execute_script("arguments[0].click();", abas[0])
            time.sleep(3)

            driver_colmeia.find_element(By.XPATH, "//*[normalize-space(text())='Arquivo']").click()
            time.sleep(1.5)
            driver_colmeia.find_element(By.XPATH, "//*[normalize-space(text())='Exportar']").click()
            time.sleep(1.5)
            driver_colmeia.find_element(By.XPATH, "//*[normalize-space(text())='Baixar como CSV UTF-8']").click()

            fim = time.time() + 20
            caminho_baixado = None
            while time.time() < fim:
                achados = glob.glob(padrao_arquivo)
                if achados:
                    caminho_baixado = achados[0]
                    break
                time.sleep(0.5)
            if not caminho_baixado:
                return None, f"Timeout esperando o download da aba '{nome_aba}'"
            return caminho_baixado, None
        finally:
            try:
                driver_colmeia.quit()
            except Exception:
                pass
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

def _ler_colmeia_eletro(caminho_csv):
    disponivel = {}
    try:
        with open(caminho_csv, "r", encoding="utf-8-sig", newline="") as f:
            leitor = csv.DictReader(f, delimiter=";")
            for linha in leitor:
                artigo = _normalizar_zeros(linha.get("ARTIGO", ""))
                if not artigo:
                    continue
                try:
                    qtd = int(float((linha.get("QUANTIDADE", "0") or "0").replace(",", ".")))
                except Exception:
                    qtd = 0
                retirado_txt = (linha.get("RETIRADO (qtd)", "") or "").strip()
                try:
                    retirado = int(float(retirado_txt.replace(",", "."))) if retirado_txt else 0
                except Exception:
                    retirado = 0
                disponivel[artigo] = disponivel.get(artigo, 0) + (qtd - retirado)
    except Exception:
        return {}
    return disponivel

def _ler_colmeia_beleza_pedidos(caminho_csv):
    pedidos = set()
    try:
        with open(caminho_csv, "r", encoding="utf-8-sig", newline="") as f:
            linhas = f.readlines()
        idx_cabecalho = next(
            (i for i, l in enumerate(linhas) if l.strip().upper().startswith("PEDIDO;")), None
        )
        if idx_cabecalho is None:
            return pedidos
        leitor = csv.DictReader(linhas[idx_cabecalho:], delimiter=";")
        for linha in leitor:
            pedido = _normalizar_zeros(linha.get("PEDIDO", ""))
            if pedido:
                pedidos.add(pedido)
    except Exception:
        return set()
    return pedidos

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# REGRAS DE PEDIDO JÁ PROCESSADO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
STATUS_QTD_DIVERGENTE = "PEDIDO JA APROVADO ANTES MAS QTD DIVERGENTE"
COLUNA_STATUS_IMPRESSAO = "STATUS IMPRESSAO"
STATUS_IMPRESSAO_MOV_RECENTE = "MOV (COM A EQUIPE, ATE 7 DIAS)"
STATUS_AVULSA_PENDENTE = "PENDENTE -- IMPRESSAO AVULSA"
STATUS_AVULSA_IMPRESSA = "IMPRESSO AVULSO"
STATUS_AVULSA_VERIFICAR = "VERIFICAR AVULSA"
STATUS_AVULSA_SEM_ARTIGO = "AVULSO - SEM ARTIGO"
STATUS_AVULSA_ERRO = "ERRO AO IMPRIMIR AVULSA, VERIFICAR PEDIDO"

def _avaliar_pedido_ja_processado(dados, base_geral, data_ciclo,
                                   colmeia_eletro=None, colmeia_beleza_pedidos=None, impressoes_robo=None):
    pedido = str(dados.get("PEDIDO", "") or "").strip()
    chave = _chave_pedido(pedido)
    if chave not in base_geral:
        return "URGENTE VERIFICAR PEDIDO NÃO ENCONTRADO NA BASE GERAL"

    validacao_artigo = str(dados.get("VALIDAÇÃO ARTIGO", "") or "").strip().upper()
    if validacao_artigo == "DIVERGENTE":
        return "ARTIGO DIVERGENTE, NAO IMPRIMIR"

    qtd_divergente = str(dados.get("STATUS", "") or "").strip().upper() == STATUS_QTD_DIVERGENTE
    data_impresso = base_geral.get(chave)
    data_robo = (impressoes_robo or {}).get(chave)
    if data_robo and (data_impresso is None or data_robo > data_impresso):
        data_impresso = data_robo
    if data_impresso and not qtd_divergente:
        dias = (data_ciclo - data_impresso).days
        if 0 <= dias <= DIAS_CONSIDERAR_RECENTE:
            return STATUS_IMPRESSAO_MOV_RECENTE

    setor = str(dados.get("DEPARTAMENTO", "") or "").strip().upper()
    if "ELETRO" in setor and colmeia_eletro is not None:
        artigo = _normalizar_zeros(dados.get("ARTIGO", ""))
        try:
            necessario = int(float(str(dados.get("AGENDADO DIA", "0") or "0").replace(",", ".")))
        except Exception:
            necessario = 0
        if necessario and colmeia_eletro.get(artigo, 0) >= necessario:
            return "COLMEIA"
    elif "BELEZA" in setor and colmeia_beleza_pedidos is not None:
        if _normalizar_zeros(pedido) in colmeia_beleza_pedidos:
            return "COLMEIA"

    return STATUS_AVULSA_PENDENTE

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# ARQUIVOS, CAMINHOS E BIN
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
PASTA_HISTORICO_APROVACAO = os.path.join(pasta_script, "HISTORICO DE APROVAÇÃO")
PASTA_IMPRESSOS           = os.path.join(pasta_script, "IMPRESSOS")
ABA_ENTRADA = "APROVAÇÃO"


LIMITE_FALHAS_IMPRESSAO_SEGUIDAS = 3


LIMITE_FALHAS_IMPRESSAO_ANTES_DO_SUCESSO = 2


_LOCAL_BASE = os.path.join(os.environ.get("LOCALAPPDATA", pasta_script), "Impressao_Bot")
PASTA_BIN   = os.path.join(_LOCAL_BASE, "Bin")
CHROME_PATH = os.path.join(PASTA_BIN, "chrome-win64",       "chrome.exe")
DRIVER_PATH = os.path.join(PASTA_BIN, "chromedriver-win64", "chromedriver.exe")


# XPaths em JSON externo > seletor ajustável quando o portal muda, sem mexer no código.
CAMINHO_XPATHS = os.path.join(pasta_script, "xpaths_impressao.json")
try:
    with open(CAMINHO_XPATHS, "r", encoding="utf-8") as _f:
        XPATHS = json.load(_f)
except Exception:
    XPATHS = {}

def _recarregar_xpaths():
    global XPATHS
    try:
        with open(CAMINHO_XPATHS, "r", encoding="utf-8") as f:
            XPATHS = json.load(f)
    except Exception:
        pass


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

NOME_CRIADOR        = os.getenv("NOME_CRIADOR",        "Rhebecca-Taih")
LINK_GITHUB_CRIADOR = os.getenv("LINK_GITHUB_CRIADOR", "https://github.com/Rhebecca-Taih")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# ARQUIVOS DE CONTROLE
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_pasta_logs    = os.path.join(pasta_script, "logs")
try:
    os.makedirs(_pasta_logs, exist_ok=True)
except Exception:
    pass

LOG_ARQUIVO          = os.path.join(_pasta_logs, "historico_impressao.txt")
LOG_ERROS_PERMANENTE = os.path.join(_pasta_logs, "historico_erros.txt")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOG
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_ui_log_callback = None

def _definir_callback_log(func):
    global _ui_log_callback
    _ui_log_callback = func

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

PASTA_LOG_LOCAL = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "RobosBureau", "Impressao")
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

def registrar_log(linhas, tag="normal"):
    sep = "-" * 60
    texto_linhas = linhas if isinstance(linhas, list) else [str(linhas)]
    hora = datetime.now().strftime("%H:%M:%S")
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
    if _ui_log_callback:
        try:
            for l in texto_linhas:
                _ui_log_callback(l, hora, tag)
        except Exception:
            pass

def registrar_erro_permanente(msg):
    try:
        with open(LOG_ERROS_PERMANENTE, "a", encoding="utf-8") as f:
            f.write(f"[{_agora_completo()}] {msg}\n")
    except Exception:
        _registrar_log_local(f"[{_agora_completo()}] ERRO: {msg}\n")


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# CHROME E BIN LOCAL
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _bin_completa():
    return os.path.exists(CHROME_PATH) and os.path.exists(DRIVER_PATH)

def _copiar_bin_da_rede():
    if _bin_completa():
        return True, ""
    if not CAMINHO_REDE_BIN:
        return False, "CAMINHO_REDE_BIN não configurado no .env"
    if not os.path.exists(CAMINHO_REDE_BIN):
        return False, f"Caminho de rede não encontrado: {CAMINHO_REDE_BIN}"
    try:
        os.makedirs(_LOCAL_BASE, exist_ok=True)
        shutil.copytree(CAMINHO_REDE_BIN, _LOCAL_BASE, dirs_exist_ok=True)
        if _bin_completa():
            return True, ""
        return False, "Cópia terminou mas os arquivos esperados não foram encontrados."
    except Exception as e:
        return False, str(e)

def _checar_chrome():
    r = {"chrome_existe": False, "driver_existe": False, "compat": False, "erro": ""}
    if not os.path.exists(CHROME_PATH):
        r["erro"] = f"Chrome não encontrado.\nCopie a pasta Bin para:\n{PASTA_BIN}"
        return r
    r["chrome_existe"] = True
    if not os.path.exists(DRIVER_PATH):
        r["erro"] = f"Chromedriver não encontrado.\nCopie a pasta Bin para:\n{PASTA_BIN}"
        return r
    r["driver_existe"] = True
    r["compat"] = True
    return r


def iniciar_navegador():
    try:
        options = Options()
        options.binary_location = CHROME_PATH
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        servico = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=servico, options=options)


        driver.set_page_load_timeout(180)
        return driver
    except Exception as e:
        registrar_log([f"❌  Erro ao abrir navegador: {e}"])
        registrar_erro_permanente(f"NAVEGADOR -- {e}")
        return None

_ultimo_erro_selenium = ""
_parar_ciclo = threading.Event()

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# AÇÕES NA PÁGINA (SELENIUM)
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def esperar(driver, xpath, condicao="visible", timeout=10):
    global _ultimo_erro_selenium
    try:
        wait = WebDriverWait(driver, timeout, poll_frequency=0.2)
        if condicao == "clickable":
            return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        if condicao == "visible":
            return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
        return None

def _preencher_campo(driver, elemento, valor):
    global _ultimo_erro_selenium
    try:
        elemento.clear()
        elemento.send_keys(valor)
        valor_atual = elemento.get_attribute("value")
        if valor_atual == valor:
            return True
        _ultimo_erro_selenium = (f"clear()+send_keys() não substituiu direito -- "
                                 f"campo ficou com {valor_atual!r} em vez de {valor!r}")
    except Exception as e:
        _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"

    try:
        driver.execute_script("""
            const el = arguments[0];
            const val = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, elemento, valor)


        if (elemento.get_attribute("value") or "") == valor:


            _ultimo_erro_selenium = ""
            return True
        _ultimo_erro_selenium = (f"JS setter também não substituiu direito -- "
                                 f"campo ficou com {(elemento.get_attribute('value') or '')!r} em vez de {valor!r}")
        return False
    except Exception as e:
        _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
        return False

_JS_CLICAR_XPATH = """
    const xpath = arguments[0];
    const el = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (!el) return 'nao_encontrado';
    const visivel = el.getClientRects().length > 0 && el.offsetParent !== null;
    if (!visivel) return 'nao_visivel';
    if (el.disabled) return 'desabilitado';
    el.scrollIntoView({block: 'nearest', inline: 'center'});
    el.click();
    return 'clicado';
"""

# Clique via JS em loop > resiste a overlay e animação; _clicar_nativo é o clique Selenium padrão.
def clicar(driver, xpath, timeout=6):
    global _ultimo_erro_selenium
    intervalo = 0.15
    tentativas = max(1, int(timeout / intervalo))
    resultado = "nao_encontrado"
    for _ in range(tentativas):
        try:
            resultado = driver.execute_script(_JS_CLICAR_XPATH, xpath)
        except Exception as e:
            _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
            return False
        if resultado == "clicado":
            return True
        time.sleep(intervalo)
    _ultimo_erro_selenium = f"elemento não ficou clicável a tempo (último estado: {resultado})"
    return False

def _clicar_nativo(driver, xpath, timeout=5):
    global _ultimo_erro_selenium
    if not xpath:
        return False
    try:
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        el.click()
        return True
    except Exception as e:
        _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
        return False

def _abrir_dropdown_config(driver, nome_campo, chave_principal, chave_fragil, timeout=4):
    if _clicar_nativo(driver, XPATHS.get(chave_principal, ""), timeout=timeout):
        return True
    if _clicar_nativo(driver, XPATHS.get(chave_fragil, ""), timeout=timeout):
        registrar_log([f"⚠️  Dropdown de {nome_campo}: XPath principal ('{chave_principal}') não funcionou -- "
                       f"XPath posicional de reserva ('{chave_fragil}') utilizado; revisar o XPath principal."])
        return True
    return False

def _fechar_modal_config_e_voltar(driver):
    if clicar(driver, XPATHS.get("btn_cancelar_config", ""), timeout=3):
        time.sleep(0.5)
    clicar(driver, XPATHS["btn_voltar"], timeout=5)

def _texto_xpath(driver, chave, timeout=5):
    el = esperar(driver, XPATHS.get(chave, ""), "presence", timeout)
    return el.text.strip() if el else ""

_MAPA_COLUNAS_DETALHE_PEDIDO = None
_XPATH_LINHA_DETALHE_PEDIDO = "//div[contains(@class,'v-table__wrapper')]//table/tbody/tr[1]"

def _resetar_mapa_colunas_detalhe_pedido():
    global _MAPA_COLUNAS_DETALHE_PEDIDO
    _MAPA_COLUNAS_DETALHE_PEDIDO = None

def _mapa_colunas_detalhe_pedido(driver, forcar=False):
    global _MAPA_COLUNAS_DETALHE_PEDIDO
    if _MAPA_COLUNAS_DETALHE_PEDIDO is not None and not forcar:
        return _MAPA_COLUNAS_DETALHE_PEDIDO
    try:
        linha = esperar(driver, _XPATH_LINHA_DETALHE_PEDIDO, "presence", 3)
        if not linha:
            return {}
        nomes = driver.execute_script(
            """
            const linha = arguments[0];
            const tabela = linha.closest('table');
            if (!tabela) return [];
            const thead = tabela.querySelector('thead');
            if (!thead) return [];
            return Array.from(thead.querySelectorAll('th')).map(th => th.textContent.trim());
            """,
            linha,
        )
        mapa = {nome.strip().lower(): i + 1 for i, nome in enumerate(nomes or []) if nome and nome.strip()}
        _MAPA_COLUNAS_DETALHE_PEDIDO = mapa
        return mapa
    except Exception:
        return {}

def _texto_celula_por_nome(driver, nome_coluna, chave_fallback, indice_linha=1, timeout=5):
    mapa = _mapa_colunas_detalhe_pedido(driver)
    indice_col = mapa.get(nome_coluna.strip().lower())
    if indice_col:
        xpath = f"//div[contains(@class,'v-table__wrapper')]//table/tbody/tr[{indice_linha}]/td[{indice_col}]"
        el = esperar(driver, xpath, "presence", timeout)
        if el:
            return el.text.strip()
    return _texto_xpath(driver, chave_fallback, timeout)

def _esperar_valor_celula_por_nome(driver, nome_coluna, chave_fallback, valores_aceitos=None, timeout=3, intervalo=0.2, indice_linha=1):
    fim = time.time() + timeout
    valor = ""
    while time.time() < fim:
        valor = _texto_celula_por_nome(driver, nome_coluna, chave_fallback, indice_linha, timeout=1)
        if valor and (not valores_aceitos or valor.upper() in valores_aceitos):
            return valor
        time.sleep(intervalo)
    return valor

def _digitar_filtro_dropdown(driver, texto):
    try:
        campo = driver.switch_to.active_element
        campo.send_keys(texto)
        return True
    except Exception:
        return False

_XPATH_OPCOES_LISTA_ABERTA = "//div[contains(@class,'v-overlay--active')]//*[@role='listbox']//*[@role='option']"

_JS_ROLAGEM_DA_LISTA = """
let el = arguments[0].parentElement;
while (el && el !== document.body) {
    const rolagem = getComputedStyle(el).overflowY;
    if ((rolagem === 'auto' || rolagem === 'scroll') && el.scrollHeight > el.clientHeight + 2) return el;
    el = el.parentElement;
}
return null;
"""

def _procurar_opcao_desenhada(driver, texto_lower):
    global _ultimo_erro_selenium
    candidatos = driver.find_elements(By.XPATH, _XPATH_OPCOES_LISTA_ABERTA)
    da_lista_aberta = bool(candidatos)
    if not candidatos:
        candidatos = driver.find_elements(By.XPATH, "//div[@role='option'] | //li")
    parcial = None
    for el in candidatos:
        try:
            texto_el = driver.execute_script("return arguments[0].textContent || '';", el).strip().lower()
            if texto_el == texto_lower:
                return el, None, candidatos, da_lista_aberta
            if parcial is None and texto_lower in texto_el:
                parcial = el
        except Exception as e:
            _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
    return None, parcial, candidatos, da_lista_aberta

def _rolar_lista_procurando(driver, lista, texto_lower):
    driver.execute_script("arguments[0].scrollTop = 0;", lista)
    time.sleep(0.25)
    texto_parcial = None
    for _ in range(200):
        exata, parcial, _, _ = _procurar_opcao_desenhada(driver, texto_lower)
        if exata is not None:
            return exata
        if parcial is not None and texto_parcial is None:
            texto_parcial = driver.execute_script("return arguments[0].textContent || '';", parcial).strip().lower()
        chegou_ao_fim = driver.execute_script(
            "const l = arguments[0]; const antes = l.scrollTop;"
            "l.scrollTop = antes + Math.max(40, l.clientHeight * 0.8);"
            "return l.scrollTop <= antes;", lista)
        if chegou_ao_fim:
            break
        time.sleep(0.25)
    if texto_parcial is None:
        return None
    return _rolar_lista_procurando(driver, lista, texto_parcial)

def _opcao_pronta_para_clique(driver, el):
    try:
        texto_el = driver.execute_script("return arguments[0].textContent || '';", el).strip().lower()
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        time.sleep(0.3)
        nova, _, _, _ = _procurar_opcao_desenhada(driver, texto_el)
        return nova if nova is not None else el
    except Exception:
        return el

def _selecionar_opcao_dropdown(driver, texto_parcial, timeout=8):
    global _ultimo_erro_selenium
    texto_lower = texto_parcial.lower()
    fim = time.time() + timeout
    while time.time() < fim:
        try:
            exata, parcial, candidatos, da_lista_aberta = _procurar_opcao_desenhada(driver, texto_lower)
            if exata is not None:
                return _opcao_pronta_para_clique(driver, exata)
            lista = None
            if da_lista_aberta:
                lista = driver.execute_script(_JS_ROLAGEM_DA_LISTA, candidatos[0])
            if lista is not None:
                achada = _rolar_lista_procurando(driver, lista, texto_lower)
                if achada is not None:
                    return _opcao_pronta_para_clique(driver, achada)
            elif parcial is not None:
                return _opcao_pronta_para_clique(driver, parcial)
        except Exception as e:
            _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
        time.sleep(0.3)
    if not _ultimo_erro_selenium:
        _ultimo_erro_selenium = "Nenhuma opção com esse texto foi encontrada na lista (sem erro de Selenium)."
    return None

def _clicar_elemento(driver, elemento):
    global _ultimo_erro_selenium
    try:
        elemento.click()
        return True
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", elemento)
            return True
        except Exception as e:
            _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
            return False

def _esperar_carregamento_sumir(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until_not(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, ".v-overlay--active, .v-progress-circular, .v-overlay__scrim")
            )
        )
    except Exception:
        pass

def _esperar_valor_input(driver, xpath, texto_esperado, timeout=3, intervalo=0.2):
    global _ultimo_erro_selenium
    if not xpath or not texto_esperado:
        return False
    esperado = texto_esperado.strip().upper()
    fim = time.time() + timeout
    valor = ""
    erro_local = None
    while time.time() < fim:
        try:
            el = driver.find_element(By.XPATH, xpath)
            valor = (el.get_attribute("value") or "").strip()
            if esperado in valor.upper():
                return True
            erro_local = None
        except Exception as e:
            erro_local = f"{type(e).__name__}: {str(e)[:300]}"
        time.sleep(intervalo)


    _ultimo_erro_selenium = erro_local or f"campo não mostrou o valor esperado '{texto_esperado}' -- ficou '{valor}'"
    return False


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# DIAGNÓSTICO DE ERRO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _pasta_erro_do_dia(agora=None):
    agora = agora or datetime.now()
    return os.path.join(_pasta_logs, "ERRO", agora.strftime("%Y"), agora.strftime("%m"), agora.strftime("%d.%m.%y"))

def _proximo_codigo_erro():
    agora = datetime.now()
    pasta_dia = _pasta_erro_do_dia(agora)
    try:
        os.makedirs(pasta_dia, exist_ok=True)
        existentes = [n for n in os.listdir(pasta_dia) if n.startswith("ERRO")]
        numeros = []
        for n in existentes:
            try:
                numeros.append(int(n.replace("ERRO", "")))
            except Exception:
                continue
        proximo = (max(numeros) + 1) if numeros else 1
    except Exception:
        proximo = 1
    nome_pasta = f"ERRO{proximo:03d}"
    codigo_legivel = f"{agora.strftime('%d.%m.%y')}_{nome_pasta}"
    return nome_pasta, codigo_legivel

def _listar_campos_da_pagina(driver):
    linhas = []
    try:
        driver.switch_to.default_content()
        contextos = [("documento principal", None)]
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for idx in range(len(iframes)):
                contextos.append((f"iframe {idx}", idx))
        except Exception:
            pass

        for nome_ctx, idx_iframe in contextos:
            try:
                driver.switch_to.default_content()
                if idx_iframe is not None:
                    iframes_atual = driver.find_elements(By.TAG_NAME, "iframe")
                    if idx_iframe >= len(iframes_atual):
                        continue
                    driver.switch_to.frame(iframes_atual[idx_iframe])
                campos = driver.find_elements(By.XPATH, "//input[@type='text' or @type='password' or not(@type)]")
                if not campos:
                    continue
                linhas.append(f"[{nome_ctx}] {len(campos)} campo(s) de input encontrado(s):")
                for c in campos:
                    try:
                        cid = c.get_attribute("id") or "(sem id)"
                        ctipo = c.get_attribute("type") or "(sem type)"
                        cvis = "visível" if c.is_displayed() else "oculto"
                        linhas.append(f"   id={cid}  type={ctipo}  {cvis}")
                    except Exception:
                        continue
            except Exception:
                continue
    except Exception:
        pass
    finally:
        try:
            driver.switch_to.default_content()
        except Exception:
            pass
    return linhas or ["Nenhum campo de input encontrado em lugar nenhum."]

def _diagnostico_pagina(driver):
    try:
        return driver.current_url, driver.title
    except Exception:
        return "?", "?"

def _capturar_diagnostico(driver, titulo, com_html=False, com_campos=False):
    nome_pasta, codigo = _proximo_codigo_erro()
    pasta = os.path.join(_pasta_erro_do_dia(), nome_pasta)
    try:
        os.makedirs(pasta, exist_ok=True)
    except Exception:
        pass

    try:
        driver.save_screenshot(os.path.join(pasta, "print.png"))
    except Exception:
        pass

    try:
        with open(os.path.join(pasta, "xpaths_carregados.json"), "w", encoding="utf-8") as f:
            json.dump(XPATHS, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    if com_html:
        try:
            with open(os.path.join(pasta, "pagina.html"), "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception:
            pass

    url_atual, titulo_pagina = _diagnostico_pagina(driver)
    linhas = [
        f"Código do erro: {codigo}",
        titulo,
        f"URL: {url_atual}",
        f"Título da página: {titulo_pagina}",
        f"Erro real do Selenium: {_ultimo_erro_selenium}",
        "(xpaths_impressao.json carregado na memória nesse instante salvo em xpaths_carregados.json, nesta mesma pasta)",
    ]
    if com_campos:
        linhas.append("Campos encontrados na página:")
        linhas.extend(_listar_campos_da_pagina(driver))

    try:
        with open(os.path.join(pasta, "log.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(linhas))
    except Exception:
        pass

    registrar_log(linhas + [f"🗂️  Diagnóstico completo em: {pasta}"], tag="erro")
    return codigo

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# BUSCA DE CAMPOS (COM FALLBACK)
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _procurar_em_iframes(driver, xpath, timeout=8, condicao="presence"):
    driver.switch_to.default_content()
    elemento = esperar(driver, xpath, condicao, timeout)
    if elemento:
        return elemento, None

    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
    except Exception:
        iframes = []

    for idx, iframe in enumerate(iframes):
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe)
            elemento = esperar(driver, xpath, condicao, 5)
            if elemento:
                return elemento, idx
        except Exception:
            continue

    driver.switch_to.default_content()
    return None, None

# XPath configurado primeiro, depois o de reserva > o aviso indica que o principal precisa de revisão.
def _procurar_campo(driver, chave_principal, chave_fallback=None, timeout=10,
                    condicao="presence", usar_iframes=False):
    xpath_principal = XPATHS.get(chave_principal, "")
    if usar_iframes:
        elemento, iframe_idx = _procurar_em_iframes(driver, xpath_principal, timeout, condicao)
    else:
        elemento = esperar(driver, xpath_principal, condicao, timeout)
        iframe_idx = None
    if elemento:
        return elemento, iframe_idx, False

    xpath_fallback = XPATHS.get(chave_fallback or "", "")
    if not xpath_fallback:
        return None, None, False

    if usar_iframes:
        elemento, iframe_idx = _procurar_em_iframes(driver, xpath_fallback, timeout, condicao)
    else:
        elemento = esperar(driver, xpath_fallback, condicao, timeout)
        iframe_idx = None
    if elemento:
        registrar_log([f"⚠️  '{chave_principal}' não encontrado pelo XPath configurado -- "
                       f"XPath de reserva (por placeholder) utilizado; revisar "
                       f"'{chave_principal}' no xpaths_impressao.json."])
        return elemento, iframe_idx, True

    return None, None, False


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# LOGIN E NAVEGAÇÃO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def fazer_login(driver):
    for tentativa in (1, 2):
        try:
            driver.get(PORTAL_URL_LOGIN)
            timeout_campo = 20 if tentativa == 1 else 35
            _esperar_carregamento_sumir(driver, timeout=timeout_campo)

            campo_user, iframe_idx, _ = _procurar_campo(
                driver, "campo_usuario", "campo_usuario_fallback",
                timeout_campo, "presence", usar_iframes=True)
            if not campo_user:
                _capturar_diagnostico(
                    driver,
                    f"⚠️  Tentativa {tentativa}/2: campo de usuário não apareceu (nem no documento principal, nem em iframes)",
                    com_html=(tentativa == 2), com_campos=(tentativa == 2)
                )
                if tentativa == 1:
                    time.sleep(3)
                    continue
                return False, "Campo de usuário não apareceu (após 2 tentativas)"
            if iframe_idx is not None:
                registrar_log([f"ℹ️  Campo de login encontrado dentro de um iframe (índice {iframe_idx})."])
            if not _preencher_campo(driver, campo_user, PORTAL_USER):
                registrar_log([f"⚠️  Tentativa {tentativa}/2: falha ao preencher o campo de usuário"])
                if tentativa == 1:
                    time.sleep(3)
                    continue
                return False, "Falha ao preencher o campo de usuário"

            campo_senha, _, _ = _procurar_campo(driver, "campo_senha", "campo_senha_fallback", 10, "presence")
            if not campo_senha:
                _capturar_diagnostico(driver, f"⚠️  Tentativa {tentativa}/2: campo de senha não apareceu")
                if tentativa == 1:
                    time.sleep(3)
                    continue
                return False, "Campo de senha não apareceu (após 2 tentativas)"
            if not _preencher_campo(driver, campo_senha, PORTAL_SENHA):
                registrar_log([f"⚠️  Tentativa {tentativa}/2: falha ao preencher o campo de senha"])
                if tentativa == 1:
                    time.sleep(3)
                    continue
                return False, "Falha ao preencher o campo de senha"

            clicar(driver, XPATHS["btn_login"])
            time.sleep(3)

            driver.switch_to.default_content()
            _esperar_carregamento_sumir(driver, timeout=15)

            campo_site, _, _ = _procurar_campo(driver, "campo_site", "campo_site_fallback", 15, "presence")
            if not campo_site:
                _capturar_diagnostico(
                    driver, f"⚠️  Tentativa {tentativa}/2: campo de Site não apareceu",
                    com_html=(tentativa == 2), com_campos=(tentativa == 2)
                )
                if tentativa == 1:
                    time.sleep(3)
                    continue
                return False, "Campo de Site não apareceu (após 2 tentativas)"

            _preencher_campo(driver, campo_site, PORTAL_SITE)
            time.sleep(1.5)
            opcao = _selecionar_opcao_dropdown(driver, PORTAL_SITE.lower())

            if not opcao or not _clicar_elemento(driver, opcao):
                _capturar_diagnostico(
                    driver, f"⚠️  Tentativa {tentativa}/2: falha ao selecionar '{PORTAL_SITE}' na lista de sites"
                )
                if tentativa == 1:
                    time.sleep(3)
                    continue
                return False, f"Falha ao selecionar o site '{PORTAL_SITE}' (após 2 tentativas)"
            time.sleep(0.5)

            clicar(driver, XPATHS["btn_entrar_site"])
            time.sleep(3)
            return True, ""

        except Exception as e:
            try:
                driver.switch_to.default_content()
            except Exception:
                pass
            if tentativa == 1:
                registrar_log([f"⚠️  Tentativa 1/2 falhou com erro inesperado: "
                              f"{type(e).__name__}: {e}. Tentando de novo..."])
                time.sleep(3)
                continue
            _capturar_diagnostico(driver, f"❌  Falha inesperada no login: {type(e).__name__}: {e}")
            return False, str(e)

    return False, "Falha desconhecida no login"

def navegar_para_impressoes_pendentes(driver):
    if not clicar(driver, XPATHS["menu_grupo_impressoes"], timeout=8):
        codigo = _capturar_diagnostico(
            driver, "❌  Falha ao clicar no menu 'Impressões' (grupo do menu não ficou clicável).",
            com_html=True
        )
        registrar_erro_permanente(f"NAVEGAÇÃO IMPRESSÕES -- menu não clicável (código {codigo})")
        return False
    time.sleep(1)

    if not clicar(driver, XPATHS["menu_item_pendentes"], timeout=8):
        codigo = _capturar_diagnostico(
            driver, "❌  Menu 'Impressões' clicado, mas 'Pendentes' não ficou clicável.",
            com_html=True
        )
        registrar_erro_permanente(f"NAVEGAÇÃO IMPRESSÕES -- item 'Pendentes' não clicável (código {codigo})")
        return False
    time.sleep(2)


    confirmou, _, _ = _procurar_campo(driver, "campo_filtrar_pedido_fallback", "campo_filtrar_pedido", 8, "presence")
    if confirmou:


        fim_poll = time.time() + 5
        while time.time() < fim_poll:
            try:
                if driver.find_elements(By.CSS_SELECTOR, "table tbody tr"):
                    break
            except Exception:
                pass
            time.sleep(0.3)
        return True

    codigo = _capturar_diagnostico(
        driver, "❌  Impressões > Pendentes clicado, mas a tela correta não foi confirmada.",
        com_html=True
    )
    registrar_erro_permanente(f"NAVEGAÇÃO IMPRESSÕES -- não confirmou a tela certa (código {codigo})")
    return False

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# FILTRO DE SITE
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
class ParadaCritica(Exception):
    pass

_JS_STATUS_FILTRO_SITE = """
    const containers = document.querySelectorAll('.v-input');
    for (const cont of containers) {
        const label = cont.querySelector('label.v-field-label, label.v-label');
        if (!label || label.textContent.trim() !== 'Site') continue;
        const selecao = cont.querySelector('.v-autocomplete__selection .truncate');
        const texto = selecao ? selecao.textContent.trim() : '';
        if (texto && !['todos', 'todos os sites', 'all'].includes(texto.toLowerCase())) {
            return {precisa: true, texto: texto};
        }
    }
    return {precisa: false, texto: ''};
"""

_JS_LIMPAR_FILTRO_SITE = """
    const containers = document.querySelectorAll('.v-input');
    for (const cont of containers) {
        const label = cont.querySelector('label.v-field-label, label.v-label');
        if (!label || label.textContent.trim() !== 'Site') continue;
        const selecao = cont.querySelector('.v-autocomplete__selection .truncate');
        const texto = selecao ? selecao.textContent.trim() : '';
        if (texto && !['todos', 'todos os sites', 'all'].includes(texto.toLowerCase())) {
            const icone = cont.querySelector("i[aria-label='Clear Site']");
            if (!icone) return 'sem_icone';
            icone.scrollIntoView({block: 'nearest', inline: 'center'});
            icone.click();
            return 'clicado';
        }
    }
    return 'nao_precisava';
"""

def _filtro_ainda_mostra_site(driver):
    try:
        resultado = driver.execute_script(_JS_STATUS_FILTRO_SITE)
        return bool(resultado and resultado.get("precisa"))
    except Exception:
        return False

def _filtro_precisa_resetar(driver):
    if _filtro_ainda_mostra_site(driver):
        return True
    time.sleep(0.4)
    return _filtro_ainda_mostra_site(driver)

def _esperar_filtro_resetar(driver, timeout=1.5, intervalo=0.2):
    fim = time.time() + timeout
    while time.time() < fim:
        if not _filtro_ainda_mostra_site(driver):
            return False
        time.sleep(intervalo)
    return _filtro_ainda_mostra_site(driver)

def _selecionar_todos_sites(driver, pedido):
    if not _filtro_precisa_resetar(driver):
        return


    if _clicar_nativo(driver, XPATHS["campo_filtro_site_pendentes"], timeout=4):
        opcao = None
        for texto_candidato in ("todos", "todos os sites", "all"):
            opcao = _selecionar_opcao_dropdown(driver, texto_candidato, timeout=3)
            if opcao:
                break
        if opcao and _clicar_elemento(driver, opcao):
            if not _esperar_filtro_resetar(driver):
                return


    try:
        driver.execute_script(_JS_LIMPAR_FILTRO_SITE)
    except Exception:
        pass
    if not _esperar_filtro_resetar(driver):
        return

    codigo_erro = _capturar_diagnostico(
        driver, f"⚠️  Filtro de Site não resetou antes de {pedido}", com_html=True
    )
    raise ParadaCritica(f"Filtro de Site não resetou antes de {pedido} (diagnóstico: {codigo_erro})")

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# SELECIONAR PEDIDO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_JS_ACHAR_ROLAR_CLICAR_OLHO = """
    const pedido = arguments[0];
    const classeIcone = arguments[1];
    const linhas = document.querySelectorAll('table tbody tr');
    for (const tr of linhas) {
        const tds = tr.querySelectorAll('td');
        let bate = false;
        for (const td of tds) {
            if (td.textContent.trim() === pedido) { bate = true; break; }
        }
        if (bate) {
            const icone = tr.querySelector(`button i.${classeIcone}, button i[class*='${classeIcone}']`);
            if (!icone) {
                return 'linha_sem_botao';
            }
            const botao = icone.closest('button');
            botao.scrollIntoView({block: 'nearest', inline: 'center'});
            botao.click();
            return 'clicado';
        }
    }
    return 'linha_nao_encontrada';
"""

_XPATH_NUMERO_DOCUMENTO = "//span[starts-with(normalize-space(.),'Nº do Documento')]/following-sibling::span[1]"

def _esperar_detalhe_do_pedido(driver, pedido, timeout=10):
    alvo = _normalizar_zeros(pedido)
    fim = time.time() + timeout
    while time.time() < fim:
        try:
            for el in driver.find_elements(By.XPATH, _XPATH_NUMERO_DOCUMENTO):
                if _normalizar_zeros(el.text) == alvo:
                    return True
        except Exception:
            pass
        time.sleep(0.3)
    return False

def _tentar_clicar_olho(driver, pedido, tentativas=10, intervalo=0.5):
    global _ultimo_erro_selenium
    classe_icone = XPATHS.get("classe_icone_olho", "mdi-eye-outline")
    motivo = "linha_nao_encontrada"
    for _ in range(tentativas):
        try:
            motivo = driver.execute_script(_JS_ACHAR_ROLAR_CLICAR_OLHO, pedido, classe_icone)
        except Exception as e:
            _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
            return False, "erro_js"
        if motivo == "clicado":
            return True, motivo
        if motivo == "linha_sem_botao":
            break
        time.sleep(intervalo)
    return False, motivo

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# DIÁLOGOS DE CONFIRMAÇÃO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_JS_CLICAR_CONFIRMACAO_DIALOGO = """
    const seletores = ['.v-overlay--active .v-card', '.v-dialog--active .v-card', "[role='dialog']"];
    for (const sel of seletores) {
        const cards = document.querySelectorAll(sel);
        for (const card of cards) {
            const botoes = Array.from(card.querySelectorAll('button')).filter(b => b.offsetParent !== null);
            if (botoes.length > 0) {
                const alvo = botoes[botoes.length - 1];
                alvo.scrollIntoView({block: 'nearest'});
                alvo.click();
                return 'clicado';
            }
        }
    }
    return 'dialogo_nao_encontrado';
"""

def _clicar_confirmacao_dialogo(driver, xpath_fragil, tentativas=6, intervalo=0.5):
    if xpath_fragil and clicar(driver, xpath_fragil, timeout=5):
        return True

    global _ultimo_erro_selenium
    for _ in range(tentativas):
        try:
            resultado = driver.execute_script(_JS_CLICAR_CONFIRMACAO_DIALOGO)
        except Exception as e:
            _ultimo_erro_selenium = f"{type(e).__name__}: {str(e)[:300]}"
            resultado = "erro_js"
        if resultado == "clicado":
            registrar_log([
                "ℹ️  Diálogo de confirmação: XPath configurado não funcionou, "
                "clique de reserva (JS) utilizado com sucesso; revisar o XPath principal."
            ])
            return True
        time.sleep(intervalo)
    return False


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# HISTÓRICO E VERSÕES
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def _pasta_historico_do_dia(setor, data_dt):
    setor = str(setor or "").strip().upper()
    return os.path.join(PASTA_HISTORICO_APROVACAO, setor,
                         data_dt.strftime("%Y"), data_dt.strftime("%m"), data_dt.strftime("%d"))

def _pasta_impressos_do_dia(setor, data_dt):
    setor = str(setor or "").strip().upper()
    return os.path.join(PASTA_IMPRESSOS, setor,
                         data_dt.strftime("%Y"), data_dt.strftime("%m"), data_dt.strftime("%d"))

# O_EXCL > duas máquinas nunca reservam o mesmo Vn.
def _reservar_proxima_versao(pasta_dia):
    os.makedirs(pasta_dia, exist_ok=True)
    numeros = []
    try:
        for nome in os.listdir(pasta_dia):
            m = re.match(r"[Vv](\d+)\.xlsx$", nome)
            if m:
                numeros.append(int(m.group(1)))
    except Exception:
        pass
    candidato = (max(numeros) + 1) if numeros else 1
    while True:
        caminho = os.path.join(pasta_dia, f"V{candidato}.xlsx")
        try:
            fd = os.open(caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return caminho
        except FileExistsError:
            candidato += 1

def ler_historico_pedidos(setor, data_dt):
    pasta_dia = _pasta_historico_do_dia(setor, data_dt)
    if not os.path.isdir(pasta_dia):
        return None, []

    arquivos_versao = []
    for nome in os.listdir(pasta_dia):
        m = re.match(r"[Vv](\d+)\.xlsx$", nome)
        if m:
            arquivos_versao.append((int(m.group(1)), os.path.join(pasta_dia, nome)))
    if not arquivos_versao:
        return None, []
    arquivos_versao.sort(key=lambda t: t[0])

    col_map_final = None
    por_pedido = {}
    for versao, caminho in arquivos_versao:
        try:
            wb = load_workbook(caminho, data_only=True)
            ws = wb[ABA_ENTRADA] if ABA_ENTRADA in wb.sheetnames else wb.active
        except Exception as e:
            registrar_log([f"⚠️  Falha ao ler {os.path.basename(caminho)}: {type(e).__name__}: {e}"])
            continue

        cabecalho = [str(c.value).strip() if c.value is not None else "" for c in ws[1]]
        col_map = {nome: idx + 1 for idx, nome in enumerate(cabecalho) if nome}
        if col_map_final is None:
            col_map_final = col_map

        col_pedido = col_map.get("PEDIDO")
        if not col_pedido:
            continue

        for linha_num in range(2, ws.max_row + 1):
            pedido_val = ws.cell(row=linha_num, column=col_pedido).value
            if pedido_val is None or not str(pedido_val).strip():
                continue
            dados = {nome: ws.cell(row=linha_num, column=idx).value for nome, idx in col_map.items()}
            por_pedido[str(pedido_val).strip()] = dados

    linhas = list(por_pedido.values())
    return col_map_final, linhas

def _salvar_impressos(col_map, linhas, setor, data_dt, caminho=None):
    if not caminho:
        caminho = _reservar_proxima_versao(_pasta_impressos_do_dia(setor, data_dt))
    wb = Workbook()
    ws = wb.active
    ws.title = ABA_ENTRADA
    for nome, idx in col_map.items():
        ws.cell(row=1, column=idx, value=nome)
    for linha_num, dados in enumerate(linhas, start=2):
        for nome, idx in col_map.items():
            ws.cell(row=linha_num, column=idx, value=dados.get(nome))
    wb.save(caminho)
    return caminho

def _verificar_impressao_recente(setor, data_dt, minutos_limite=40):
    pasta_dia = _pasta_impressos_do_dia(setor, data_dt)
    if not os.path.isdir(pasta_dia):
        return False, None, None
    mais_recente = None
    try:
        for nome in os.listdir(pasta_dia):
            if re.match(r"[Vv]\d+\.xlsx$", nome):
                try:
                    mtime = os.path.getmtime(os.path.join(pasta_dia, nome))
                except Exception:
                    continue
                if mais_recente is None or mtime > mais_recente:
                    mais_recente = mtime
    except Exception:
        return False, None, None
    if mais_recente is None:
        return False, None, None
    idade_min = (time.time() - mais_recente) / 60
    if idade_min < minutos_limite:
        hora_texto = datetime.fromtimestamp(mais_recente).strftime("%d/%m/%Y %H:%M")
        return True, idade_min, hora_texto
    return False, None, None

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# PROCESSAMENTO -- IMPRESSÃO NORMAL
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def processar_pedido_impressao(driver, dados, modelo, impressora):
    pedido = str(dados.get("PEDIDO", "") or "").strip()
    if not pedido:
        return "SEM NUMERO DE PEDIDO"

    _resetar_mapa_colunas_detalhe_pedido()
    registrar_log([f"🖨️  Processando pedido {pedido}"])

    if modelo == MODELO_DETECCAO_AUTOMATICA:
        modelo_detectado = _resolver_modelo_automatico(dados)
        if not modelo_detectado:
            registrar_log([f"⚠️  {pedido}: detecção automática não conseguiu determinar um modelo válido "
                           f"(VALIDAÇÃO MODELO='{dados.get('VALIDAÇÃO MODELO', '') }') -- pulando, revisar manualmente."])
            return "MODELO NAO DETECTADO, VERIFICAR"
        registrar_log([f"🔎  {pedido}: modelo detectado automaticamente -- '{modelo_detectado}'"])
        modelo = modelo_detectado


    _tempos = []
    _t_ref = [time.perf_counter()]
    def _marca(nome):
        agora = time.perf_counter()
        _tempos.append(f"{nome}={agora - _t_ref[0]:.2f}s")
        _t_ref[0] = agora

    try:


        campo, _, _ = _procurar_campo(driver, "campo_filtrar_pedido_fallback", "campo_filtrar_pedido", 8, "visible")
        _marca("achar_campo_busca")
        if not campo:
            _capturar_diagnostico(driver, f"❌  {pedido}: campo de busca não apareceu", com_html=True)
            return "ERRO BUSCA"
        if not _preencher_campo(driver, campo, pedido):
            _capturar_diagnostico(driver, f"❌  {pedido}: falha ao preencher o campo de busca", com_html=True)
            return "ERRO BUSCA"
        _marca("preencher_busca")

        _selecionar_todos_sites(driver, pedido)
        _marca("reset_site")


        clicou, motivo = _tentar_clicar_olho(driver, pedido)
        _marca("olho_1a_tentativa")
        if not clicou and motivo == "linha_nao_encontrada":
            registrar_log([f"🔄  {pedido}: busca não filtrou na primeira tentativa -- tentando de novo..."])
            if _preencher_campo(driver, campo, pedido):
                clicou, motivo = _tentar_clicar_olho(driver, pedido)
            _marca("olho_retry")

        if not clicou:
            _capturar_diagnostico(
                driver, f"⚠️  {pedido}: não apareceu na lista de Pendentes após a busca ({motivo})", com_html=True
            )
            return "NAO ACHOU"

        if not _esperar_detalhe_do_pedido(driver, pedido):
            _capturar_diagnostico(
                driver, f"⚠️  {pedido}: a página aberta pelo ícone de detalhes não corresponde ao pedido (Nº do Documento não confere)",
                com_html=True
            )
            clicar(driver, XPATHS["btn_voltar"], timeout=5)
            return "ERRO AO ABRIR PEDIDO"
        _marca("abrir_pedido")


        status_abertura = _esperar_valor_celula_por_nome(driver, "Status", "confer_status").upper()
        _marca("status_abertura")
        if status_abertura != "NOVO":


            registrar_log([f"ℹ️  {pedido}: status ao abrir é '{status_abertura or '?'}' (não NOVO; esperado "
                           f"NOVO, já que o Aprovador marcou como aprovado) -- status original mantido, sem impressão."])
            dados["_STATUS_NO_PORTAL"] = status_abertura
            clicar(driver, XPATHS["btn_voltar"], timeout=5)
            return "JA_AVANCOU_NO_SITE"


        etiqueta_atual   = _texto_celula_por_nome(driver, "Etiqueta", "confer_etiqueta")
        impressora_atual = _texto_celula_por_nome(driver, "Impressora", "confer_impressora")
        etiqueta_ok   = etiqueta_atual.strip().upper() == modelo.strip().upper()
        impressora_ok = impressora_atual.strip().upper() == impressora.strip().upper()
        _marca("conferir_config_atual")

        if etiqueta_ok and impressora_ok:
            registrar_log([f"ℹ️  {pedido}: Etiqueta '{etiqueta_atual}' e Impressora '{impressora_atual}' "
                           f"já estavam corretas -- configuração mantida."])
        else:
            if not clicar(driver, XPATHS["btn_configuracao"], timeout=6):
                _capturar_diagnostico(driver, f"❌  {pedido}: falha ao abrir a configuração (engrenagem)", com_html=True)
                clicar(driver, XPATHS["btn_voltar"], timeout=5)
                return "ERRO CONFIGURACAO"


            esperar(driver, XPATHS.get("btn_salvar_config_fragil", ""), "clickable", 4)
            _marca("abrir_config")


            if not etiqueta_ok:
                if not _abrir_dropdown_config(driver, "Etiqueta", "dropdown_etiqueta", "dropdown_etiqueta_fragil"):
                    _capturar_diagnostico(driver, f"❌  {pedido}: falha ao abrir o dropdown de Etiqueta", com_html=True)
                    _fechar_modal_config_e_voltar(driver)
                    return "ERRO CONFIGURACAO"
                opcao_etiqueta = _selecionar_opcao_dropdown(driver, modelo, timeout=5)
                if not opcao_etiqueta or not _clicar_elemento(driver, opcao_etiqueta):
                    _capturar_diagnostico(driver, f"❌  {pedido}: opção de Etiqueta '{modelo}' não localizada na lista", com_html=True)
                    _fechar_modal_config_e_voltar(driver)
                    return "ERRO CONFIGURACAO"
                _marca("selecionar_etiqueta")


                if not _esperar_valor_input(driver, XPATHS.get("campo_etiqueta_input", ""), modelo, timeout=3):
                    _capturar_diagnostico(driver, f"❌  {pedido}: escolhi a Etiqueta '{modelo}' mas o campo não confirmou a mudança", com_html=True)
                    _fechar_modal_config_e_voltar(driver)
                    return "ERRO CONFIGURACAO"

            if not impressora_ok:
                if not _abrir_dropdown_config(driver, "Impressora", "dropdown_impressora", "dropdown_impressora_fragil"):
                    _capturar_diagnostico(driver, f"❌  {pedido}: falha ao abrir o dropdown de Impressora", com_html=True)
                    _fechar_modal_config_e_voltar(driver)
                    return "ERRO CONFIGURACAO"
                opcao_impressora = _selecionar_opcao_dropdown(driver, impressora, timeout=5)
                if not opcao_impressora or not _clicar_elemento(driver, opcao_impressora):
                    _capturar_diagnostico(driver, f"❌  {pedido}: opção de Impressora '{impressora}' não localizada na lista", com_html=True)
                    _fechar_modal_config_e_voltar(driver)
                    return "ERRO CONFIGURACAO"
                _marca("selecionar_impressora")


                if not _esperar_valor_input(driver, XPATHS.get("campo_impressora_input", ""), impressora, timeout=3):
                    _capturar_diagnostico(driver, f"❌  {pedido}: escolhi a Impressora '{impressora}' mas o campo não confirmou a mudança", com_html=True)
                    _fechar_modal_config_e_voltar(driver)
                    return "ERRO CONFIGURACAO"

            if (not _esperar_valor_input(driver, XPATHS.get("campo_etiqueta_input", ""), modelo, timeout=2)
                    or not _esperar_valor_input(driver, XPATHS.get("campo_impressora_input", ""), impressora, timeout=2)):
                _capturar_diagnostico(driver, f"❌  {pedido}: antes de salvar, Etiqueta/Impressora já não estavam com "
                                              f"'{modelo}' / '{impressora}' -- configuração não salva", com_html=True)
                _fechar_modal_config_e_voltar(driver)
                return "ERRO CONFIGURACAO"

            if not _clicar_confirmacao_dialogo(driver, XPATHS.get("btn_salvar_config_fragil", "")):
                _capturar_diagnostico(driver, f"❌  {pedido}: falha ao salvar a configuração (Etiqueta/Impressora)", com_html=True)
                _fechar_modal_config_e_voltar(driver)
                return "ERRO CONFIGURACAO"


            etiqueta_gravada, impressora_gravada = "", ""
            fim_poll = time.time() + 15
            proximo_atualizar = 0
            while time.time() < fim_poll:
                if time.time() >= proximo_atualizar:
                    if not clicar(driver, XPATHS.get("btn_atualizar_lista", ""), timeout=3):
                        _clicar_texto(driver, "Atualizar", timeout=2)
                    _esperar_carregamento_sumir(driver, timeout=4)
                    proximo_atualizar = time.time() + 4
                etiqueta_gravada   = _texto_celula_por_nome(driver, "Etiqueta", "confer_etiqueta", timeout=1)
                impressora_gravada = _texto_celula_por_nome(driver, "Impressora", "confer_impressora", timeout=1)
                if (modelo.strip().upper() in etiqueta_gravada.upper()
                        and impressora.strip().upper() in impressora_gravada.upper()):
                    break
                time.sleep(0.5)
            _marca("salvar_config")

            if modelo.strip().upper() not in etiqueta_gravada.upper() or impressora.strip().upper() not in impressora_gravada.upper():
                _capturar_diagnostico(
                    driver,
                    f"⚠️  {pedido}: configuração salva divergente -- esperado Etiqueta='{modelo}' / Impressora='{impressora}', "
                    f"linha mostra Etiqueta='{etiqueta_gravada}' / Impressora='{impressora_gravada}'",
                    com_html=True
                )
                clicar(driver, XPATHS["btn_voltar"], timeout=5)
                return "ERRO CONFIGURACAO NAO CONFERE"


        status_pre_imprimir = _texto_celula_por_nome(driver, "Status", "confer_status").upper()
        if status_pre_imprimir and status_pre_imprimir != "NOVO":
            registrar_log([f"ℹ️  {pedido}: status virou '{status_pre_imprimir}' antes do clique em Imprimir (mudou no site) -- "
                           f"status original mantido, sem impressão."])
            dados["_STATUS_NO_PORTAL"] = status_pre_imprimir
            clicar(driver, XPATHS["btn_voltar"], timeout=5)
            return "JA_AVANCOU_NO_SITE"

        if not clicar(driver, XPATHS["btn_imprimir"], timeout=6):
            _capturar_diagnostico(driver, f"❌  {pedido}: falha ao clicar em Imprimir", com_html=True)
            clicar(driver, XPATHS["btn_voltar"], timeout=5)
            return "ERRO IMPRIMIR"


        status_final = ""
        fim_poll = time.time() + 6
        while time.time() < fim_poll:
            status_final = _texto_celula_por_nome(driver, "Status", "confer_status").upper()
            if status_final and status_final != "NOVO":
                break
            time.sleep(0.3)
        _marca("imprimir")

        if status_final not in ("INICIADO", "FINALIZADO"):


            _capturar_diagnostico(
                driver,
                f"⚠️  {pedido}: status não confirmou a impressão (mostra '{status_final or '?'}', "
                f"esperado INICIADO/FINALIZADO).",
                com_html=True
            )
            registrar_log([f"⚠️  {pedido}: impressão não confirmada pelo site."], tag="aviso")
            clicar(driver, XPATHS["btn_voltar"], timeout=5)
            _marca("voltar")
            return "ERRO AO IMPRIMIR, VERIFICAR PEDIDO"

        registrar_log([f"✅  {pedido}: impresso com sucesso (status no site: {status_final})"], tag="ok")
        clicar(driver, XPATHS["btn_voltar"], timeout=5)
        _marca("voltar")
        return "IMPRESSO"
    finally:
        if _tempos:
            registrar_log([f"⏱️  {pedido}: " + " | ".join(_tempos)])


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# IMPRESSÃO AVULSA
# Avulsa busca por rótulo visível > a tela não tem a estrutura estável da tela de Pendentes.
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
_JS_NORM = "const norm = s => (s||'').replace(/\\s+/g,' ').trim().toLowerCase();"

_JS_ACHAR_CAMPO_ROTULO = _JS_NORM + """
    const rot = norm(arguments[0]);
    for (const inp of document.querySelectorAll('input, textarea')) {
        if (inp.type === 'hidden' || inp.getClientRects().length === 0) continue;
        const cont = inp.closest('.v-input, .v-field, .v-text-field') || inp.parentElement;
        let lab = '';
        if (cont) { const l = cont.querySelector('label, .v-label, .v-field-label'); if (l) lab = norm(l.textContent); }
        if (norm(inp.getAttribute('placeholder')) === rot || norm(inp.getAttribute('aria-label')) === rot || lab === rot) return inp;
    }
    return null;
"""

_JS_CLICAR_TEXTO = _JS_NORM + """
    const alvo = norm(arguments[0]), exato = arguments[1];
    let melhor = null, tam = 1e9;
    for (const el of document.querySelectorAll('button, a, [role=button], [role=menuitem], [role=tab], .v-btn, .v-list-item, .v-list-item-title, span, div, p')) {
        if (el.getClientRects().length === 0) continue;
        const t = norm(el.textContent);
        if (!t || t.length > 80) continue;
        if (exato ? t !== alvo : !t.includes(alvo)) continue;
        if (t.length < tam) { melhor = el; tam = t.length; }
    }
    if (!melhor) return 'nao_encontrado';
    const btn = melhor.closest('button, .v-btn');
    if (btn && (btn.disabled || btn.classList.contains('v-btn--disabled'))) return 'desabilitado';
    melhor.scrollIntoView({block: 'nearest'});
    melhor.click();
    return 'clicado';
"""

_JS_CLICAR_LUPA = """
    const inp = arguments[0];
    const cont = inp.closest('.v-input, .v-field, .v-text-field');
    if (!cont) return 'sem_container';
    const alvo = cont.querySelector('.v-field__append-inner button, .v-field__append-inner .v-icon, .v-field__append-inner i, .v-field__append-inner svg, .v-field__append-inner');
    if (!alvo) return 'sem_lupa';
    alvo.click();
    return 'clicado';
"""

_JS_LINHAS_MODAL = _JS_NORM + """
    const dlgs = [...document.querySelectorAll('[role=dialog], .v-dialog, .v-overlay--active .v-overlay__content')].filter(d => d.getClientRects().length > 0);
    for (const d of dlgs) {
        const tabela = d.querySelector('table');
        if (!tabela) continue;
        const ths = [...tabela.querySelectorAll('thead th')].map(th => norm(th.textContent));
        let iSku = ths.indexOf('sku');
        if (iSku < 0) iSku = 0;
        const linhas = [...tabela.querySelectorAll('tbody tr')].filter(tr => tr.querySelector('td'));
        return linhas.map(tr => { const td = tr.querySelectorAll('td')[iSku]; return td ? (td.textContent || '').trim() : ''; });
    }
    return null;
"""

_JS_CLICAR_ACAO_LINHA = _JS_NORM + """
    const idx = arguments[0];
    const dlgs = [...document.querySelectorAll('[role=dialog], .v-dialog, .v-overlay--active .v-overlay__content')].filter(d => d.getClientRects().length > 0);
    for (const d of dlgs) {
        const tabela = d.querySelector('table');
        if (!tabela) continue;
        const ths = [...tabela.querySelectorAll('thead th')].map(th => norm(th.textContent));
        let iAcao = ths.findIndex(t => t === 'ações' || t === 'acoes' || t === 'ação' || t === 'acao');
        const linhas = [...tabela.querySelectorAll('tbody tr')].filter(tr => tr.querySelector('td'));
        const tr = linhas[idx];
        if (!tr) return 'sem_linha';
        const tds = tr.querySelectorAll('td');
        const td = iAcao >= 0 && tds[iAcao] ? tds[iAcao] : tds[tds.length - 1];
        const alvo = td.querySelector('button, [role=button], .v-icon, i, svg') || td;
        alvo.click();
        return 'clicado';
    }
    return 'sem_modal';
"""

# Varre elementos pequenos atrás do aviso > a tela de avulsa não tem seletor fixo de aviso.
_JS_AVISOS = _JS_NORM + """
    const saida = [];
    for (const el of document.querySelectorAll('*')) {
        if (el.children.length > 3 || el.getClientRects().length === 0) continue;
        const t = (el.textContent || '').replace(/\\s+/g, ' ').trim();
        if (!t || t.length > 160) continue;
        if (/sucesso|success|erro|falha|error|fail|n[aã]o foi poss/i.test(t)) saida.push(t);
    }
    return [...new Set(saida)];
"""

def _campo_por_rotulo(driver, rotulo):
    try:
        return driver.execute_script(_JS_ACHAR_CAMPO_ROTULO, rotulo)
    except Exception:
        return None

def _esperar_campo_por_rotulo(driver, rotulo, timeout=8):
    fim = time.time() + timeout
    while time.time() < fim:
        el = _campo_por_rotulo(driver, rotulo)
        if el is not None:
            return el
        time.sleep(0.3)
    return None

def _clicar_texto(driver, texto, exato=True, timeout=6):
    fim = time.time() + timeout
    resultado = "nao_encontrado"
    while time.time() < fim:
        try:
            resultado = driver.execute_script(_JS_CLICAR_TEXTO, texto, exato)
        except Exception:
            return False
        if resultado == "clicado":
            return True
        time.sleep(0.3)
    return False

def _texto_do_campo(driver, el):
    try:
        return driver.execute_script(
            "const c = arguments[0].closest('.v-input, .v-field') || arguments[0].parentElement;"
            "return ((arguments[0].value || '') + ' ' + (c ? c.textContent : '')).toLowerCase();", el) or ""
    except Exception:
        return ""

def _abrir_pagina_impressao_avulsa(driver):


    if not _clicar_texto(driver, "Impressão Avulsa", timeout=2):
        if not _clicar_texto(driver, "Impressões", timeout=6):
            return False
        time.sleep(1)
        if not _clicar_texto(driver, "Impressão Avulsa", timeout=6):
            return False
    return _esperar_campo_por_rotulo(driver, "Buscar por SKU", timeout=15) is not None

def _limpar_pagina_avulsa(driver):
    _clicar_texto(driver, "Limpar", timeout=3)
    time.sleep(0.6)

def _buscar_e_selecionar_sku(driver, artigo6):
    campo = _esperar_campo_por_rotulo(driver, "Buscar por SKU", timeout=6)
    if campo is None or not _preencher_campo(driver, campo, artigo6):
        return False
    try:
        r = driver.execute_script(_JS_CLICAR_LUPA, campo)
    except Exception:
        r = "erro"
    if r != "clicado":
        try:
            campo.send_keys(Keys.ENTER)
        except Exception:
            return False

    linhas = None
    fim = time.time() + 10
    while time.time() < fim:
        try:
            linhas = driver.execute_script(_JS_LINHAS_MODAL)
        except Exception:
            linhas = None
        if linhas:
            break
        time.sleep(0.4)
    if not linhas:
        _fechar_modal_produto(driver)
        return False

    skus = [str(s).strip() for s in linhas]
    escolhido = None
    for criterio in (lambda s: s == artigo6 + "0000", lambda s: s == artigo6, lambda s: s[:6] == artigo6):
        escolhido = next((i for i, s in enumerate(skus) if criterio(s)), None)
        if escolhido is not None:
            break
    if escolhido is not None:
        try:
            return driver.execute_script(_JS_CLICAR_ACAO_LINHA, escolhido) == "clicado"
        except Exception:
            return False
    _fechar_modal_produto(driver)
    return False

def _fechar_modal_produto(driver):
    _clicar_texto(driver, "Cancelar", timeout=3)
    time.sleep(0.6)

def _escolher_opcao_v_select(driver, rotulo, texto):
    campo = _esperar_campo_por_rotulo(driver, rotulo, timeout=6)
    if campo is None:
        return False
    try:
        campo.click()
    except Exception:
        return False
    _digitar_filtro_dropdown(driver, texto)
    opcao = _selecionar_opcao_dropdown(driver, texto, timeout=5)
    if not opcao or not _clicar_elemento(driver, opcao):
        return False
    time.sleep(0.4)
    campo = _campo_por_rotulo(driver, rotulo) or campo
    return texto.lower() in _texto_do_campo(driver, campo)

def _imprimir_e_confirmar(driver):
    try:
        antes = set(driver.execute_script(_JS_AVISOS) or [])
    except Exception:
        antes = set()
    fim_botao = time.time() + 6
    clicou = False
    while time.time() < fim_botao:
        if _clicar_texto(driver, "Imprimir", timeout=1):
            clicou = True
            break
        time.sleep(0.4)
    if not clicou:
        return "botao", ""
    fim = time.time() + 12
    while time.time() < fim:
        try:
            novos = [t for t in (driver.execute_script(_JS_AVISOS) or []) if t not in antes]
        except Exception:
            novos = []
        for t in novos:
            if re.search(r"erro|falha|error|fail|n[aã]o foi poss", t, re.I):
                return "erro", t
        for t in novos:
            if re.search(r"sucesso|success", t, re.I):
                return "ok", t
        time.sleep(0.3)
    return "sem_aviso", ""

def processar_pedido_avulso(driver, dados, modelo, impressora):
    pedido = str(dados.get("PEDIDO", "") or "").strip()
    artigo6 = re.sub(r"\.0$", "", str(dados.get("ARTIGO", "") or "").strip())[:6]
    registrar_log([f"🖨️  {pedido}: impressão avulsa (artigo {artigo6})"])

    if modelo == MODELO_DETECCAO_AUTOMATICA:
        modelo_pedido = _resolver_modelo_automatico(dados)
        if not modelo_pedido:
            registrar_log([f"⚠️  {pedido}: modelo não detectado -- sem impressão."])
            return "MODELO NAO DETECTADO, VERIFICAR"
    else:
        modelo_pedido = modelo
    try:
        qtd = int(float(str(dados.get("AGENDADO DIA", "0") or "0").replace(",", ".")))
    except Exception:
        qtd = 0
    if not artigo6 or qtd <= 0:
        registrar_log([f"⚠️  {pedido}: artigo ou quantidade inválidos (artigo='{artigo6}', qtd={qtd})."])
        return STATUS_AVULSA_ERRO

    selecionou = False
    for tentativa in (1, 2):
        _limpar_pagina_avulsa(driver)
        if not _buscar_e_selecionar_sku(driver, artigo6):
            registrar_log([f"⚠️  {pedido}: artigo {artigo6} não encontrado na busca (tentativa {tentativa}/2)."])
            continue
        time.sleep(0.8)
        campo_sku = _campo_por_rotulo(driver, "Buscar por SKU")
        sku_tela = (campo_sku.get_attribute("value") or "").strip() if campo_sku is not None else ""
        if sku_tela[:6] == artigo6:
            selecionou = True
            break
        registrar_log([f"⚠️  {pedido}: SKU na tela ('{sku_tela}') diverge do artigo {artigo6} (tentativa {tentativa}/2)."])
    if not selecionou:
        _capturar_diagnostico(driver, f"⚠️  {pedido}: avulsa -- artigo {artigo6} não localizado", com_html=True)
        return STATUS_AVULSA_SEM_ARTIGO

    if not _escolher_opcao_v_select(driver, "Etiqueta", modelo_pedido):
        _capturar_diagnostico(driver, f"❌  {pedido}: avulsa -- falha ao escolher a Etiqueta '{modelo_pedido}'", com_html=True)
        return STATUS_AVULSA_ERRO
    if not _escolher_opcao_v_select(driver, "Impressora", impressora):
        _capturar_diagnostico(driver, f"❌  {pedido}: avulsa -- falha ao escolher a Impressora '{impressora}'", com_html=True)
        return STATUS_AVULSA_ERRO

    campo_qtd = _esperar_campo_por_rotulo(driver, "Quantidade", timeout=5)
    if campo_qtd is None or not _preencher_campo(driver, campo_qtd, str(qtd)):
        _capturar_diagnostico(driver, f"❌  {pedido}: avulsa -- falha ao preencher a Quantidade {qtd}", com_html=True)
        return STATUS_AVULSA_ERRO

    campo_doc = _campo_por_rotulo(driver, "Documento Fiscal")
    if campo_doc is None:
        _clicar_texto(driver, "Dados de Produção", exato=False, timeout=4)
        campo_doc = _esperar_campo_por_rotulo(driver, "Documento Fiscal", timeout=5)
    if campo_doc is None or not _preencher_campo(driver, campo_doc, pedido):
        _capturar_diagnostico(driver, f"❌  {pedido}: avulsa -- falha ao preencher o Documento Fiscal", com_html=True)
        return STATUS_AVULSA_ERRO

    resultado, texto = _imprimir_e_confirmar(driver)
    if resultado == "ok":
        registrar_log([f"✅  {pedido}: impressão avulsa confirmada pelo site ('{texto}')"], tag="ok")
        return STATUS_AVULSA_IMPRESSA
    if resultado == "botao":
        _capturar_diagnostico(driver, f"❌  {pedido}: avulsa -- botão Imprimir não ficou clicável", com_html=True)
        return STATUS_AVULSA_ERRO
    if resultado == "erro":
        _capturar_diagnostico(driver, f"❌  {pedido}: avulsa -- site avisou erro: '{texto}'", com_html=True)
        return STATUS_AVULSA_ERRO
    _capturar_diagnostico(driver, f"⚠️  {pedido}: avulsa -- Imprimir acionado, mas nenhum aviso apareceu (sem reimpressão)", com_html=True)
    return STATUS_AVULSA_VERIFICAR

def _registrar_tela_jobs_impressao(driver):
    try:
        if _clicar_texto(driver, "Jobs de Impressão", timeout=5):
            time.sleep(3)
            _capturar_diagnostico(driver, "📋  Tela 'Jobs de Impressão' após 1ª impressão avulsa (evidência)", com_html=True)
    except Exception:
        pass

def _ler_status_avulsa_anteriores(setor, data_dt):
    pasta = _pasta_impressos_do_dia(setor, data_dt)
    finais = {STATUS_AVULSA_IMPRESSA, STATUS_AVULSA_VERIFICAR}
    versoes = []
    try:
        for nome in os.listdir(pasta):
            m = re.match(r"[Vv](\d+)\.xlsx$", nome)
            if m:
                versoes.append((int(m.group(1)), os.path.join(pasta, nome)))
    except Exception:
        return {}
    ultimo = {}
    for _, caminho in sorted(versoes):
        try:
            wb = load_workbook(caminho, data_only=True, read_only=True)
            ws = wb[ABA_ENTRADA] if ABA_ENTRADA in wb.sheetnames else wb.active
            linhas = ws.iter_rows(values_only=True)
            cab = [str(c).strip() if c is not None else "" for c in next(linhas)]
            if "PEDIDO" not in cab or "STATUS" not in cab or COLUNA_STATUS_IMPRESSAO not in cab:
                wb.close()
                continue
            ip, is_, ii = cab.index("PEDIDO"), cab.index("STATUS"), cab.index(COLUNA_STATUS_IMPRESSAO)
            for row in linhas:
                if len(row) > max(ip, is_, ii) and row[ip] is not None:
                    ultimo[str(row[ip]).strip()] = (str(row[is_] or "").strip(), str(row[ii] or "").strip())
            wb.close()
        except Exception:
            continue
    return {p: v for p, v in ultimo.items() if v[1] in finais}

def _ler_impressos_do_lote(setor, data_dt):
    pasta = _pasta_impressos_do_dia(setor, data_dt)
    ja_impressos_status = {"IMPRESSO", STATUS_AVULSA_IMPRESSA}
    versoes = []
    try:
        for nome in os.listdir(pasta):
            m = re.match(r"[Vv](\d+)\.xlsx$", nome)
            if m:
                versoes.append((int(m.group(1)), os.path.join(pasta, nome)))
    except Exception:
        return {}
    encontrados = {}
    for numero, caminho in sorted(versoes):
        try:
            wb = load_workbook(caminho, data_only=True, read_only=True)
            ws = wb[ABA_ENTRADA] if ABA_ENTRADA in wb.sheetnames else wb.active
            linhas = ws.iter_rows(values_only=True)
            cab = [str(c).strip() if c is not None else "" for c in next(linhas)]
            if "PEDIDO" not in cab or COLUNA_STATUS_IMPRESSAO not in cab:
                wb.close()
                continue
            ip, ii = cab.index("PEDIDO"), cab.index(COLUNA_STATUS_IMPRESSAO)
            for row in linhas:
                if len(row) > max(ip, ii) and row[ip] is not None:
                    status_imp = str(row[ii] or "").strip()
                    if status_imp in ja_impressos_status:
                        encontrados.setdefault(str(row[ip]).strip(), (status_imp, f"V{numero}"))
            wb.close()
        except Exception:
            continue
    return encontrados

def _impressoes_do_robo_nos_lotes_anteriores(setor, data_dt):
    datas = {}
    for dias_antes in range(1, DIAS_CONSIDERAR_RECENTE + 1):
        data_lote = data_dt - timedelta(days=dias_antes)
        for pedido in _ler_impressos_do_lote(setor, data_lote):
            chave = _chave_pedido(pedido)
            if chave not in datas or data_lote > datas[chave]:
                datas[chave] = data_lote
    return datas

# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# CICLO DE IMPRESSÃO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
def processar_ciclo_impressao(data_texto, setor, modelo, impressora):
    _recarregar_xpaths()
    data_dt = datetime.strptime(data_texto, "%d/%m/%Y")

    col_map, linhas = ler_historico_pedidos(setor, data_dt)
    if not linhas:
        registrar_log([f"ℹ️  Nenhum pedido encontrado em HISTORICO DE APROVAÇÃO "
                       f"para {setor} / {data_texto}."])
        return {"ok": True, "critico": False, "motivo": "Nenhum pedido encontrado para essa Data/Setor.",
                "total": 0, "aprovados": 0, "impressos": 0, "ja_processados": 0, "erros": 0}

    if COLUNA_STATUS_IMPRESSAO not in col_map:
        col_map = dict(col_map)
        col_map[COLUNA_STATUS_IMPRESSAO] = max(col_map.values()) + 1

    ja_impressos_lote = _ler_impressos_do_lote(setor, data_dt)
    for d in linhas:
        chave_ped = str(d.get("PEDIDO", "") or "").strip()
        if chave_ped not in ja_impressos_lote:
            continue
        status_anterior, versao = ja_impressos_lote[chave_ped]
        d["STATUS"] = "SIM"
        d[COLUNA_STATUS_IMPRESSAO] = status_anterior
        registrar_log([f"ℹ️  {chave_ped}: já impresso nesse lote ({status_anterior}, {versao}) -- sem reimpressão."])


    elegiveis   = sum(1 for d in linhas if str(d.get("STATUS", "") or "").strip().upper().startswith("APROVADO"))


    pedidos_mov = [d for d in linhas
                   if str(d.get("STATUS", "") or "").strip().upper() in ("MOV", STATUS_QTD_DIVERGENTE)]
    registrar_log([f"📊  {len(linhas)} pedido(s) encontrado(s) para {setor} / {data_texto} "
                   f"({elegiveis} aprovado(s), {len(pedidos_mov)} MOV/qtd divergente, "
                   f"{len(linhas) - elegiveis - len(pedidos_mov)} com outro status)."])


    mov_classificados = 0


    ja_avulsa = _ler_status_avulsa_anteriores(setor, data_dt) if pedidos_mov else {}
    if ja_avulsa:
        restantes = []
        for d in pedidos_mov:
            chave_ped = str(d.get("PEDIDO", "") or "").strip()
            if chave_ped in ja_avulsa:
                d["STATUS"], d[COLUNA_STATUS_IMPRESSAO] = ja_avulsa[chave_ped]
                registrar_log([f"ℹ️  {chave_ped}: já passou pela impressão avulsa antes ({ja_avulsa[chave_ped][1]}) -- sem reimpressão."])
            else:
                restantes.append(d)
        pedidos_mov = restantes
    referencias = {}

    def _carregar_referencias(pedidos):
        if "base_geral" not in referencias:
            referencias["base_geral"] = None
            ok_copia, erro_copia = _copiar_base_geral_local()
            if not ok_copia:
                registrar_log([f"⚠️  Falha ao copiar a BASE GERAL da rede -- {len(pedidos)} pedido(s) "
                               f"ficam sem classificar nesse ciclo: {erro_copia}"])
                registrar_erro_permanente(f"CÓPIA BASE GERAL -- {erro_copia}")
            else:
                referencias["base_geral"] = _ler_base_geral_pedidos()
                if referencias["base_geral"] is None:
                    registrar_log([f"⚠️  Falha ao ler a cópia local da BASE GERAL -- {len(pedidos)} pedido(s) "
                                   f"ficam sem classificar nesse ciclo."])
                    registrar_erro_permanente("LER BASE GERAL LOCAL -- retornou None (falha de leitura)")
            referencias["robo"] = _impressoes_do_robo_nos_lotes_anteriores(setor, data_dt)
        if referencias["base_geral"] is None:
            return False

        setores_presentes = {str(d.get("DEPARTAMENTO", "") or "").strip().upper() for d in pedidos}
        if any("ELETRO" in s for s in setores_presentes) and "colmeia_eletro" not in referencias:
            referencias["colmeia_eletro"] = None
            caminho_eletro, erro_eletro = _baixar_colmeia_aba("ELETRO")
            if caminho_eletro:
                referencias["colmeia_eletro"] = _ler_colmeia_eletro(caminho_eletro)
            else:
                registrar_log([f"⚠️  Falha ao baixar a Colmeia de Artigos (ELETRO): {erro_eletro}"])
                registrar_erro_permanente(f"COLMEIA ELETRO -- {erro_eletro}")
        if any("BELEZA" in s for s in setores_presentes) and "colmeia_beleza" not in referencias:
            referencias["colmeia_beleza"] = None
            caminho_beleza, erro_beleza = _baixar_colmeia_aba("BELEZA")
            if caminho_beleza:
                referencias["colmeia_beleza"] = _ler_colmeia_beleza_pedidos(caminho_beleza)
            else:
                registrar_log([f"⚠️  Falha ao baixar a Colmeia de Artigos (BELEZA): {erro_beleza}"])
                registrar_erro_permanente(f"COLMEIA BELEZA -- {erro_beleza}")
        return True

    def _classificar_ja_processados(pedidos):
        if not pedidos or not _carregar_referencias(pedidos):
            return 0
        alterados = 0
        for dados_mov in pedidos:
            resultado_mov = _avaliar_pedido_ja_processado(
                dados_mov, referencias["base_geral"], data_dt,
                colmeia_eletro=referencias.get("colmeia_eletro"),
                colmeia_beleza_pedidos=referencias.get("colmeia_beleza"),
                impressoes_robo=referencias["robo"])
            if str(dados_mov.get(COLUNA_STATUS_IMPRESSAO, "") or "") != resultado_mov:
                dados_mov[COLUNA_STATUS_IMPRESSAO] = resultado_mov
                alterados += 1
                registrar_log([f"📦  {dados_mov.get('PEDIDO', '?')}: {resultado_mov}"])
        return alterados

    mov_classificados += _classificar_ja_processados(pedidos_mov)

    pendentes_avulsa = [d for d in pedidos_mov
                        if str(d.get(COLUNA_STATUS_IMPRESSAO, "") or "").strip() == STATUS_AVULSA_PENDENTE]
    avulsas_impressas = 0

    if elegiveis == 0 and not pendentes_avulsa:


        if mov_classificados > 0:
            try:
                caminho_salvo = _salvar_impressos(col_map, linhas, setor, data_dt)
                registrar_log([f"🏁  {mov_classificados} pedido(s) MOV classificado(s). Resultado salvo em: {caminho_salvo}"])
            except Exception as e:
                registrar_log([f"❌  Erro ao salvar resultado em IMPRESSOS: {e}"])
                registrar_erro_permanente(f"SALVAR IMPRESSOS -- {type(e).__name__}: {e}")
        else:
            registrar_log(["ℹ️  Nenhum pedido aprovado nesse lote -- nada para imprimir. Nada novo para salvar em IMPRESSOS."])
        return {"ok": True, "critico": False, "motivo": "Nenhum pedido aprovado nesse lote -- nada para imprimir.",
                "total": len(linhas), "aprovados": 0, "impressos": 0, "ja_processados": 0, "erros": 0}


    if not _bin_completa():
        registrar_log(["🔧  Primeira vez nesse PC -- copiando Chrome/Driver da rede "
                       "(pode levar alguns minutos, só acontece uma vez)..."])
    ok_bin, erro_bin = _copiar_bin_da_rede()
    if not ok_bin:
        registrar_log([f"❌  {erro_bin}"])
        registrar_erro_permanente(f"BIN -- {erro_bin}")
        return {"ok": False, "critico": False, "motivo": erro_bin,
                "total": len(linhas), "aprovados": elegiveis, "impressos": 0, "ja_processados": 0, "erros": 0}

    driver = iniciar_navegador()
    if not driver:
        return {"ok": False, "critico": False, "motivo": "Falha ao abrir o navegador.",
                "total": len(linhas), "aprovados": elegiveis, "impressos": 0, "ja_processados": 0, "erros": 0}

    ok_login, erro_login = fazer_login(driver)
    if not ok_login:
        registrar_log([f"❌  Falha no login: {erro_login}"])
        registrar_erro_permanente(f"LOGIN -- {erro_login}")
        try: driver.quit()
        except Exception: pass
        return {"ok": False, "critico": False, "motivo": f"Falha no login: {erro_login}",
                "total": len(linhas), "aprovados": elegiveis, "impressos": 0, "ja_processados": 0, "erros": 0}

    if elegiveis > 0 and not navegar_para_impressoes_pendentes(driver):
        try: driver.quit()
        except Exception: pass
        return {"ok": False, "critico": False, "motivo": "Falha ao navegar até Impressões > Pendentes.",
                "total": len(linhas), "aprovados": elegiveis, "impressos": 0, "ja_processados": 0, "erros": 0}

    impressos, ja_processados, erros = 0, 0, 0
    falhas_impressao_seguidas = 0
    critico, motivo_critico, categoria_critica = False, "", ""

    arquivo_da_rodada = {"caminho": None}

    def _salvar_parcial():
        try:
            arquivo_da_rodada["caminho"] = _salvar_impressos(col_map, linhas, setor, data_dt,
                                                             arquivo_da_rodada["caminho"])
        except Exception as e:
            registrar_log([f"⚠️  Falha ao gravar o IMPRESSOS agora ({type(e).__name__}: {e}) -- "
                           f"nova tentativa no próximo pedido e no fim."], tag="aviso")
            registrar_erro_permanente(f"SALVAR IMPRESSOS PARCIAL -- {type(e).__name__}: {e}")

    for dados in linhas:
        if _parar_ciclo.is_set():
            registrar_log(["⏹  Processo parado pelo usuário (o pedido em andamento terminou antes)."], tag="aviso")
            critico, categoria_critica = True, "parado_usuario"
            motivo_critico = "Parado pelo usuário. O pedido que estava em andamento terminou antes da parada."
            break
        try:
            driver.title
        except WebDriverException as e:
            registrar_log([f"🛑  CICLO INTERROMPIDO: a sessão do navegador morreu ({type(e).__name__})."])
            registrar_erro_permanente(f"CICLO INTERROMPIDO -- sessão do navegador morreu ({type(e).__name__}: {e})")
            critico = True
            categoria_critica = "sessao_navegador"
            motivo_critico = f"A sessão do navegador morreu no meio do processo ({type(e).__name__})."
            break


        status_atual = str(dados.get("STATUS", "") or "").strip().upper()
        if not status_atual.startswith("APROVADO"):
            continue

        try:
            status = processar_pedido_impressao(driver, dados, modelo, impressora)
            if status == "JA_AVANCOU_NO_SITE":
                dados[COLUNA_STATUS_IMPRESSAO] = (f"JA ESTAVA {dados.get('_STATUS_NO_PORTAL') or '?'} "
                                                  f"NO PORTAL, VERIFICAR")
                ja_processados += 1
            elif status == "IMPRESSO":
                dados["STATUS"] = "SIM"
                dados[COLUNA_STATUS_IMPRESSAO] = "IMPRESSO"
            else:
                dados[COLUNA_STATUS_IMPRESSAO] = status
            if status == "IMPRESSO":
                impressos += 1
                falhas_impressao_seguidas = 0
                _salvar_parcial()
            elif status == "JA_AVANCOU_NO_SITE":
                pass
            elif status == "ERRO AO IMPRIMIR, VERIFICAR PEDIDO":
                erros += 1
                falhas_impressao_seguidas += 1


                limite = (LIMITE_FALHAS_IMPRESSAO_ANTES_DO_SUCESSO if impressos == 0
                          else LIMITE_FALHAS_IMPRESSAO_SEGUIDAS)
                if falhas_impressao_seguidas >= limite:
                    if impressos == 0:
                        registrar_log([f"🛑  CICLO INTERROMPIDO: {limite} pedidos seguidos não confirmaram a "
                                       f"impressão, e nenhum pedido foi impresso com sucesso ainda nesse ciclo -- "
                                       f"provável falha do agente/software de impressão desde o início."], tag="erro")
                        motivo_critico = (f"{limite} pedidos seguidos não confirmaram a impressão, e nenhum "
                                          f"pedido foi impresso com sucesso neste ciclo ainda. Verifique o "
                                          f"agente de impressão antes de tentar de novo.")
                    else:
                        registrar_log([f"🛑  CICLO INTERROMPIDO: {limite} pedidos seguidos não confirmaram a "
                                       f"impressão -- provável falha do agente/software de impressão no meio "
                                       f"do lote (já tinha impresso {impressos} com sucesso antes)."], tag="erro")
                        motivo_critico = (f"{limite} pedidos seguidos não confirmaram a impressão, mesmo já "
                                          f"tendo impresso {impressos} com sucesso antes nesse ciclo. Verifique "
                                          f"o agente de impressão antes de tentar de novo.")
                    registrar_erro_permanente(f"PARADA CRÍTICA IMPRESSÃO -- {falhas_impressao_seguidas} falhas "
                                              f"seguidas (impressos antes: {impressos})")
                    critico = True
                    categoria_critica = "agente_impressao"
                    break


            else:
                erros += 1
        except ParadaCritica as e:


            registrar_log([f"🛑  CICLO INTERROMPIDO: {e}"], tag="erro")
            registrar_erro_permanente(f"PARADA CRÍTICA -- {e}")
            critico = True
            categoria_critica = "filtro_site"
            motivo_critico = str(e)
            break
        except WebDriverException as e:
            registrar_log([f"🛑  CICLO INTERROMPIDO: a sessão do navegador morreu processando um pedido ({type(e).__name__})."])
            registrar_erro_permanente(f"CICLO INTERROMPIDO -- sessão do navegador morreu ({type(e).__name__}: {e})")
            critico = True
            categoria_critica = "sessao_navegador"
            motivo_critico = f"A sessão do navegador morreu no meio do processo ({type(e).__name__})."
            break
        except Exception as e:
            registrar_erro_permanente(f"PROCESSAR PEDIDO {dados.get('PEDIDO','?')} -- {type(e).__name__}: {e}")
            dados[COLUNA_STATUS_IMPRESSAO] = "ERRO"
            erros += 1


    ja_avancados_no_portal = [d for d in linhas if d.get("_STATUS_NO_PORTAL")]
    if ja_avancados_no_portal and not critico:
        registrar_log([f"🔎  {len(ja_avancados_no_portal)} pedido(s) aprovado(s) já não estavam NOVO no portal -- "
                       f"conferindo a última impressão (BASE GERAL e IMPRESSOS dos últimos {DIAS_CONSIDERAR_RECENTE} dias)."])
        mov_classificados += _classificar_ja_processados(ja_avancados_no_portal)
        pendentes_avulsa = pendentes_avulsa + [
            d for d in ja_avancados_no_portal
            if str(d.get(COLUNA_STATUS_IMPRESSAO, "") or "").strip() == STATUS_AVULSA_PENDENTE]

    if pendentes_avulsa and not critico:
        registrar_log([f"🖨️  Impressão avulsa: {len(pendentes_avulsa)} pedido(s) pendente(s)."])
        if not _abrir_pagina_impressao_avulsa(driver):
            _capturar_diagnostico(driver, "❌  Falha ao abrir Impressões > Impressão Avulsa.", com_html=True)
            registrar_erro_permanente("NAVEGAÇÃO IMPRESSÃO AVULSA -- página não abriu")
            erros += len(pendentes_avulsa)
        else:
            erros_avulsa_seguidos = 0
            jobs_registrado = False
            for dados in pendentes_avulsa:
                if _parar_ciclo.is_set():
                    registrar_log(["⏹  Impressão avulsa parada pelo usuário (o pedido em andamento terminou antes)."], tag="aviso")
                    critico, categoria_critica = True, "parado_usuario"
                    motivo_critico = "Parado pelo usuário. O pedido que estava em andamento terminou antes da parada."
                    break
                try:
                    driver.title
                    novo_status = processar_pedido_avulso(driver, dados, modelo, impressora)
                except WebDriverException as e:
                    registrar_log([f"🛑  Impressão avulsa interrompida: sessão do navegador morreu ({type(e).__name__})."])
                    registrar_erro_permanente(f"AVULSA -- sessão do navegador morreu ({type(e).__name__}: {e})")
                    critico, categoria_critica = True, "sessao_navegador"
                    motivo_critico = f"A sessão do navegador morreu na impressão avulsa ({type(e).__name__})."
                    break
                except Exception as e:
                    registrar_erro_permanente(f"AVULSA PEDIDO {dados.get('PEDIDO','?')} -- {type(e).__name__}: {e}")
                    novo_status = STATUS_AVULSA_ERRO
                if novo_status == STATUS_AVULSA_IMPRESSA:
                    dados["STATUS"] = "SIM"
                dados[COLUNA_STATUS_IMPRESSAO] = novo_status
                mov_classificados += 1
                if novo_status == STATUS_AVULSA_IMPRESSA:
                    avulsas_impressas += 1
                    erros_avulsa_seguidos = 0
                    _salvar_parcial()
                    if not jobs_registrado:
                        jobs_registrado = True
                        _registrar_tela_jobs_impressao(driver)
                        _abrir_pagina_impressao_avulsa(driver)
                elif novo_status in (STATUS_AVULSA_ERRO, STATUS_AVULSA_VERIFICAR):
                    erros += 1
                    erros_avulsa_seguidos += 1
                    if erros_avulsa_seguidos >= 3:
                        registrar_log(["🛑  Impressão avulsa interrompida: 3 falhas seguidas -- revisar a tela/impressora."], tag="erro")
                        registrar_erro_permanente("AVULSA -- 3 falhas seguidas, ciclo avulso interrompido")
                        break
                else:
                    erros_avulsa_seguidos = 0

    try:
        driver.quit()
    except Exception:
        pass


    if impressos > 0 or mov_classificados > 0 or ja_processados > 0:
        try:
            caminho_salvo = _salvar_impressos(col_map, linhas, setor, data_dt, arquivo_da_rodada["caminho"])
            registrar_log([f"🏁  Resultado salvo em: {caminho_salvo}"])
        except Exception as e:
            registrar_log([f"❌  Erro ao salvar resultado em IMPRESSOS: {e}"])
            registrar_erro_permanente(f"SALVAR IMPRESSOS -- {type(e).__name__}: {e}")
    else:
        registrar_log(["ℹ️  Nenhum pedido impresso nesse ciclo -- nada novo para salvar em IMPRESSOS."])

    return {
        "ok": not critico, "critico": critico, "motivo": motivo_critico, "categoria_critica": categoria_critica,
        "total": len(linhas), "aprovados": elegiveis,
        "impressos": impressos, "ja_processados": ja_processados, "erros": erros,
        "mov_classificados": mov_classificados, "avulsas_impressas": avulsas_impressas,
    }


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# JANELA DE IMPRESSÃO
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
class JanelaImpressao:
    FONTE_TITULO  = ("Segoe UI", 17, "bold")
    FONTE_SUB     = ("Segoe UI", 12)
    FONTE_ROTULO  = ("Segoe UI", 10, "bold")
    FONTE_TEXTO   = ("Segoe UI", 13)
    FONTE_PEQUENA = ("Segoe UI", 10)

    ICONES_LOG = {"ok": "✅", "aviso": "⚠️", "erro": "❌", "normal": "🔹"}

    def __init__(self):
        _gerenciar_log()


        self.estado = "verificando"
        self._resultado_ciclo = None
        self._info_recente = None

        self.root = ctk.CTk()
        self.root.title("Robô de Impressão")
        self.root.configure(fg_color=COR_FUNDO)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        self.setor_selecionado     = tk.StringVar(master=self.root, value="")
        self.modelo_selecionado    = tk.StringVar(master=self.root, value=MODELO_DETECCAO_AUTOMATICA)
        self.impressora_selecionada = tk.StringVar(master=self.root, value="")

        self._construir_ui_boot()
        self._centralizar(560, 720)
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

        badge = ctk.CTkLabel(hdr, text="🖨️", font=("Segoe UI", 20),
                             fg_color=COR_HEADER, text_color=COR_HEADER_TXT,
                             corner_radius=12, width=44, height=44)
        badge.pack(side="left")

        txt_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        txt_hdr.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(txt_hdr, text="Robô de Impressão", font=self.FONTE_TITULO,
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

        self._falha_lib = False
        self._falha_chrome = False
        self.root.after(0, lambda: self._ir_para_etapa("bibliotecas"))

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
            self._mostrar_continuar("Próximo: Pasta Bin (Chrome/Driver)", "bin")
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


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA 2 -- bin (Chrome/Driver)
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_bin(self):
        card = self._card("Pasta Bin (Chrome/Driver locais)")
        self._lbl_bin_status = ctk.CTkLabel(card, text="Verificando...", font=("Segoe UI", 11),
                                            text_color=COR_TEXTO, anchor="w")
        self._lbl_bin_status.pack(anchor="w")
        self._lbl_bin_detalhe = ctk.CTkLabel(card, text="", font=("Segoe UI", 9),
                                             text_color=COR_MUTED, anchor="w",
                                             wraplength=460, justify="left")
        self._lbl_bin_detalhe.pack(anchor="w", pady=(4, 0))
        threading.Thread(target=self._checar_bin, daemon=True).start()

    def _checar_bin(self):
        if _bin_completa():
            self.root.after(0, lambda: self._lbl_bin_status.configure(
                text="✅  Já existe localmente.", text_color=COR_OK))
            self.root.after(300, lambda: self._mostrar_continuar("Próximo: Chrome e Driver", "chrome_driver"))
            return

        self.root.after(0, lambda: self._lbl_bin_status.configure(
            text="⏳  Copiando da rede...", text_color=COR_AVISO))
        self.root.after(0, lambda: self._lbl_bin_detalhe.configure(
            text=f"Origem: {CAMINHO_REDE_BIN}\nIsso pode demorar vários minutos, aguarde..."))

        parar_ticker = threading.Event()
        inicio_copia = time.time()

        def _ticker():
            while not parar_ticker.is_set():
                decorrido = int(time.time() - inicio_copia)
                try:
                    self.root.after(0, lambda d=decorrido: self._lbl_bin_status.configure(
                        text=f"⏳  Copiando Bin... {d//60}min {d%60}s"))
                except Exception:
                    return
                time.sleep(1)

        threading.Thread(target=_ticker, daemon=True).start()
        ok_copia, erro_copia = _copiar_bin_da_rede()
        parar_ticker.set()

        if ok_copia:
            self.root.after(0, lambda: self._lbl_bin_status.configure(
                text="✅  Bin copiada com sucesso.", text_color=COR_OK))
            self.root.after(0, lambda: self._lbl_bin_detalhe.configure(text=""))
        else:
            self.root.after(0, lambda: self._lbl_bin_status.configure(
                text="❌  Falha ao copiar Bin da rede.", text_color=COR_ERRO))
            self.root.after(0, lambda: self._lbl_bin_detalhe.configure(text=erro_copia[:200]))
            registrar_erro_permanente(f"CÓPIA BIN -- {erro_copia}")

        self.root.after(300, lambda: self._mostrar_continuar("Próximo: Chrome e Driver", "chrome_driver"))


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA 3 -- Chrome e Driver
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_chrome_driver(self):
        card = self._card("Chrome e Driver")
        cr = _checar_chrome()

        linhas = []
        linhas.append(("✅  Chrome encontrado (local)", COR_OK) if cr["chrome_existe"]
                      else ("❌  Chrome não encontrado", COR_ERRO))
        linhas.append(("✅  Driver encontrado (local)", COR_OK) if cr["driver_existe"]
                      else ("❌  Driver não encontrado", COR_ERRO))
        if cr["compat"]:
            linhas.append(("✅  Compatíveis", COR_OK))

        for texto, cor in linhas:
            ctk.CTkLabel(card, text=texto, font=("Segoe UI", 11), text_color=cor,
                        anchor="w").pack(anchor="w", pady=2)

        if not cr["chrome_existe"] or not cr["driver_existe"]:
            for l in cr["erro"].split("\n"):
                if l.strip():
                    ctk.CTkLabel(card, text=l.strip(), font=("Segoe UI", 9),
                                text_color=COR_MUTED, anchor="w").pack(anchor="w")

        self._falha_chrome = not cr["compat"]
        self._mostrar_continuar("Pronto para iniciar!", "final")


    # ─── ⋆⋅☆⋅⋆ ───
    # ETAPA FINAL -- iniciar
    # ─── ⋆⋅☆⋅⋆ ───
    def _etapa_final(self):
        card = self._card()
        falha = self._falha_lib or self._falha_chrome
        if falha:
            ctk.CTkLabel(card, text="⚠️  Alguns itens tiveram problema -- revise antes de iniciar.",
                        font=("Segoe UI", 11), text_color=COR_AVISO, anchor="w",
                        wraplength=460, justify="left").pack(anchor="w")
            ctk.CTkButton(self.frm_controle, text="🔄  Reiniciar", font=("Segoe UI", 11, "bold"),
                         fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT, hover_color=COR_BORDA,
                         corner_radius=8, height=36,
                         command=self._reiniciar_programa).pack(fill="x", pady=(6, 0))
            return

        ctk.CTkLabel(card, text="✅  Tudo certo! Pronto para iniciar.",
                    font=("Segoe UI", 13, "bold"), text_color=COR_OK, anchor="w").pack(anchor="w")
        ctk.CTkButton(self.frm_controle, text="▶  Iniciar", font=("Segoe UI", 12, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=8, height=38,
                     command=self._entrar_no_app).pack(fill="x", pady=(6, 0))

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

    def _entrar_no_app(self):
        for w in self.root.winfo_children():
            w.destroy()
        self._construir_ui_principal()
        self.estado = "pronto"
        self._renderizar_estado()


    def _construir_ui_principal(self):
        self._cabecalho(self.root, "Impressão de etiquetas dos pedidos aprovados")


        self.frm_controle = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.frm_controle.pack(fill="both", expand=True, padx=24)


        self.frm_rodape = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frm_rodape.pack(fill="x", padx=24, pady=(4, 20))
        ctk.CTkButton(self.frm_rodape, text="✖  Fechar", font=self.FONTE_PEQUENA,
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, width=100, height=32,
                     command=self._ao_fechar).pack(side="right")
        ctk.CTkButton(self.frm_rodape, text="📄  Abrir log", font=self.FONTE_PEQUENA,
                     fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO,
                     hover_color=COR_BORDA, corner_radius=8, width=120, height=32,
                     command=self._abrir_log).pack(side="right", padx=(0, 8))

    def _abrir_log(self):
        try:
            os.startfile(LOG_ARQUIVO)
        except Exception as e:
            registrar_erro_permanente(f"ABRIR LOG -- {type(e).__name__}: {e}")

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
            pass
        elif self.estado == "pronto":
            self._tela_pronto()
        elif self.estado == "recente":
            self._tela_recente()
        elif self.estado == "processando":
            self._tela_processando()
        elif self.estado == "concluido":
            self._tela_concluido()
        elif self.estado == "erro":
            self._tela_erro()
        elif self.estado == "erro_critico":
            self._tela_erro_critico()


    def _tela_pronto(self):
        card_data = self._card("Data dos pedidos")
        linha_data = ctk.CTkFrame(card_data, fg_color="transparent")
        linha_data.pack(fill="x")

        self.var_data = tk.StringVar(master=self.root, value=getattr(self, "_ultima_data", ""))
        ctk.CTkLabel(linha_data, text="📅", font=("Segoe UI", 14),
                    text_color="#B8860B", width=20).pack(side="left", padx=(0, 8))
        ctk.CTkEntry(linha_data, textvariable=self.var_data,
                    font=self.FONTE_TEXTO, fg_color=COR_FUNDO,
                    border_width=1, border_color=COR_BORDA,
                    text_color=COR_TEXTO, corner_radius=8,
                    width=160, height=34, placeholder_text="dd/mm/aaaa").pack(side="left")
        self.var_data.trace_add("write", lambda *a: self._validar_pronto())

        ctk.CTkButton(linha_data, text="📆 Escolher", font=self.FONTE_PEQUENA,
                     fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO,
                     hover_color=COR_BORDA, corner_radius=8, width=90, height=34,
                     command=self._abrir_calendario).pack(side="left", padx=(8, 0))

        card_setor = self._card("Setor")
        self._botoes_setor = self._grade_opcoes(
            card_setor, SETORES_DISPONIVEIS, self.setor_selecionado, colunas=2,
            icones={"ELETRO-ELETRONICOS": "💡", "BELEZA": "✨"})

        card_modelo = self._card("Etiqueta / Modelo")
        self._botoes_modelo = self._grade_opcoes(
            card_modelo, MODELOS_DISPONIVEIS, self.modelo_selecionado, colunas=2)

        card_impressora = self._card("Impressora")
        self._botoes_impressora = self._grade_opcoes(
            card_impressora, IMPRESSORAS_DISPONIVEIS, self.impressora_selecionada, colunas=2)

        self.btn_processar = ctk.CTkButton(
            self.frm_controle, text="▶  Processar", font=("Segoe UI", 14, "bold"),
            fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
            text_color_disabled=COR_HEADER_TXT,
            corner_radius=10, height=46, state="disabled",
            command=self._iniciar_processamento
        )
        self.btn_processar.pack(fill="x", pady=(4, 0))

        self._validar_pronto()

    def _grade_opcoes(self, parent, opcoes, variavel, colunas=2, icones=None):
        icones = icones or {}
        frm = ctk.CTkFrame(parent, fg_color="transparent")
        frm.pack(fill="x")
        botoes = {}

        def _selecionar(nome):
            variavel.set(nome)
            for n, b in botoes.items():
                if n == nome:
                    b.configure(fg_color=COR_CHIP_ATIVO, text_color=COR_HEADER_TXT, hover_color="#E6B325")
                else:
                    b.configure(fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO, hover_color=COR_BORDA)
            self._validar_pronto()

        for i, opt in enumerate(opcoes):
            rotulo = f"{icones[opt]}  {opt}" if opt in icones else opt
            b = ctk.CTkButton(
                frm, text=rotulo, font=self.FONTE_PEQUENA,
                fg_color=COR_CHIP_INATIVO, text_color=COR_TEXTO,
                hover_color=COR_BORDA, corner_radius=8, height=38,
                command=lambda o=opt: _selecionar(o)
            )
            b.grid(row=i // colunas, column=i % colunas, sticky="ew", padx=4, pady=4)
            botoes[opt] = b
        for c in range(colunas):
            frm.grid_columnconfigure(c, weight=1)

        if variavel.get() and variavel.get() in botoes:
            _selecionar(variavel.get())
        return botoes

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

    def _validar_pronto(self):
        pode = (bool(self.var_data.get().strip()) and bool(self.setor_selecionado.get())
                and bool(self.modelo_selecionado.get()) and bool(self.impressora_selecionada.get())
                and _IMPORTS_OK)
        try:
            self.btn_processar.configure(state="normal" if pode else "disabled")
        except Exception:
            pass


    def _tela_recente(self):
        info = self._info_recente or {}
        card = self._card()
        ctk.CTkLabel(card, text="⏳  Essa Data/Setor foi processada recentemente",
                    font=("Segoe UI", 13, "bold"), text_color=COR_AVISO, anchor="w",
                    wraplength=460, justify="left").pack(anchor="w")
        detalhe = (f"Data: {info.get('data','?')}   |   Setor: {info.get('setor','?')}\n"
                  f"Último processamento: {info.get('quando','?')} (há {info.get('minutos','?')} min)")
        ctk.CTkLabel(card, text=detalhe, font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    anchor="w", justify="left").pack(anchor="w", pady=(6, 4))
        ctk.CTkLabel(card,
                    text="Confira se ninguém está processando esse lote agora. Os pedidos já "
                         "impressos nesse lote são pulados.",
                    font=self.FONTE_PEQUENA, text_color=COR_MUTED,
                    anchor="w", wraplength=460, justify="left").pack(anchor="w", pady=(0, 12))
        ctk.CTkButton(self.frm_controle, text="↩  Voltar", font=("Segoe UI", 12, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=8, height=40,
                     command=lambda: self._mudar_estado("pronto")).pack(fill="x")
        ctk.CTkButton(self.frm_controle, text="▶  Processar mesmo assim", font=self.FONTE_PEQUENA,
                     fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, height=34,
                     command=self._confirmar_processar_recente).pack(fill="x", pady=(8, 0))

    def _confirmar_processar_recente(self):
        import tkinter.messagebox as _mb
        info = self._info_recente or {}
        confirmar = _mb.askyesno(
            "Processar novamente",
            f"Tem certeza que deseja processar esse lote novamente?\n\n"
            f"Data: {info.get('data', '?')}  |  Setor: {info.get('setor', '?')}\n"
            f"Último processamento há {info.get('minutos', '?')} min."
        )
        if confirmar:
            self._iniciar_processamento(forcar=True)


    def _tela_processando(self):
        card = self._card()
        ctk.CTkLabel(card, text="⚙️  Processando...", font=("Segoe UI", 13, "bold"),
                    text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card,
                    text=(f"Data: {self.var_data.get()}   |   Setor: {self.setor_selecionado.get()}\n"
                          f"Etiqueta: {self.modelo_selecionado.get()}   |   Impressora: {self.impressora_selecionada.get()}"),
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE,
                    anchor="w", justify="left").pack(anchor="w", pady=(6, 0))
        barra = ctk.CTkProgressBar(card, height=6, corner_radius=4,
                                   fg_color=COR_FUNDO, progress_color=COR_HEADER,
                                   mode="indeterminate")
        barra.pack(fill="x", pady=(12, 0))
        barra.start()

        if _parar_ciclo.is_set():
            ctk.CTkLabel(card, text="⏹  Parando depois do pedido atual...", font=self.FONTE_PEQUENA,
                        text_color=COR_AVISO, anchor="w").pack(anchor="w", pady=(10, 0))
        else:
            ctk.CTkButton(self.frm_controle, text="⏹  Parar", font=self.FONTE_PEQUENA,
                         fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                         hover_color=COR_BORDA, corner_radius=8, height=34,
                         command=self._parar_processamento).pack(fill="x")

    def _parar_processamento(self):
        import tkinter.messagebox as _mb
        confirmar = _mb.askyesno(
            "Parar impressão",
            "O robô termina o pedido em andamento e para antes do próximo.\n\n"
            "O que já foi impresso fica salvo em IMPRESSOS.\n\nParar agora?"
        )
        if confirmar and self.estado == "processando":
            _parar_ciclo.set()
            registrar_log(["⏹  Parada pedida pelo usuário -- aguardando o pedido em andamento terminar."], tag="aviso")
            self._renderizar_estado()


    def _tela_concluido(self):
        r = self._resultado_ciclo or {}
        card = self._card()
        ctk.CTkLabel(card, text="✅  Processamento concluído!", font=("Segoe UI", 14, "bold"),
                    text_color=COR_OK, anchor="w").pack(anchor="w")
        ctk.CTkLabel(card,
                    text=f"Data: {self.var_data.get()}   |   Setor: {self.setor_selecionado.get()}",
                    font=self.FONTE_PEQUENA, text_color=COR_DETALHE, anchor="w").pack(anchor="w", pady=(6, 8))
        resumo = (f"Pedidos do dia: {r.get('total',0)}   (aprovados: {r.get('aprovados',0)})\n"
                 f"Impressos: {r.get('impressos',0)}\n"
                 f"Já impressos antes (conferir): {r.get('ja_processados',0)}\n"
                 f"Com erro: {r.get('erros',0)}")
        ctk.CTkLabel(card, text=resumo, font=self.FONTE_PEQUENA, text_color=COR_TEXTO,
                    anchor="w", justify="left").pack(anchor="w", pady=(0, 4))
        ctk.CTkButton(self.frm_controle, text="🔄  Nova impressão", font=("Segoe UI", 14, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=10, height=46,
                     command=self._resetar_para_nova_impressao).pack(fill="x")
        self._botao_reenviar_mesma_data()


    def _tela_erro(self):
        card = self._card()
        ctk.CTkLabel(card, text="⚠️  Processamento não concluído",
                    font=("Segoe UI", 14, "bold"), text_color=COR_AVISO, anchor="w",
                    wraplength=460, justify="left").pack(anchor="w")
        r = self._resultado_ciclo or {}
        ctk.CTkLabel(card, text=r.get("motivo", ""), font=self.FONTE_PEQUENA, text_color=COR_MUTED,
                    anchor="w", wraplength=460, justify="left").pack(anchor="w", pady=(6, 12))
        ctk.CTkButton(self.frm_controle, text="🔄  Tentar novamente", font=("Segoe UI", 14, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=10, height=46,
                     command=lambda: self._mudar_estado("pronto")).pack(fill="x")
        self._botao_reenviar_mesma_data()


    _TEXTO_ERRO_CRITICO = {
        "agente_impressao": ("🛑  Processo interrompido -- verifique o agente de impressão",
                             "🔄  Tentar novamente (depois de checar o agente)"),
        "filtro_site":      ("🛑  Processo interrompido -- filtro de Site não resetou",
                             "🔄  Tentar novamente"),
        "sessao_navegador": ("🛑  Processo interrompido -- o navegador travou ou fechou",
                             "🔄  Tentar novamente"),
        "parado_usuario":   ("⏹  Processo parado pelo usuário",
                             "↩  Voltar ao início"),
    }
    _TEXTO_ERRO_CRITICO_PADRAO = ("🛑  Processo interrompido", "🔄  Tentar novamente")

    def _tela_erro_critico(self):
        card = self._card()
        r = self._resultado_ciclo or {}
        titulo, texto_botao = self._TEXTO_ERRO_CRITICO.get(
            r.get("categoria_critica", ""), self._TEXTO_ERRO_CRITICO_PADRAO)
        ctk.CTkLabel(card, text=titulo,
                    font=("Segoe UI", 14, "bold"), text_color=COR_ERRO, anchor="w",
                    wraplength=460, justify="left").pack(anchor="w")
        ctk.CTkLabel(card, text=r.get("motivo", ""), font=self.FONTE_PEQUENA, text_color=COR_MUTED,
                    anchor="w", wraplength=460, justify="left").pack(anchor="w", pady=(6, 6))


        _impressos_parada = r.get('impressos', 0)
        resumo = f"Impressos até a parada: {_impressos_parada} de {r.get('aprovados',0)} aprovados\n"
        resumo += ("O resultado parcial já foi salvo em IMPRESSOS." if _impressos_parada > 0
                   else "Nenhum pedido foi impresso ainda -- nada foi salvo em IMPRESSOS.")
        ctk.CTkLabel(card, text=resumo, font=self.FONTE_PEQUENA, text_color=COR_TEXTO,
                    anchor="w", justify="left").pack(anchor="w", pady=(0, 12))
        ctk.CTkButton(self.frm_controle, text=texto_botao,
                     font=("Segoe UI", 13, "bold"),
                     fg_color=COR_HEADER, text_color=COR_HEADER_TXT, hover_color="#E6B325",
                     corner_radius=10, height=46,
                     command=lambda: self._mudar_estado("pronto")).pack(fill="x")
        self._botao_reenviar_mesma_data()

    def _botao_reenviar_mesma_data(self):
        ctk.CTkButton(self.frm_controle, text="🔁  Imprimir novamente a mesma Data/Setor",
                     font=self.FONTE_PEQUENA, fg_color=COR_BTN_C, text_color=COR_BTN_C_TXT,
                     hover_color=COR_BORDA, corner_radius=8, height=34,
                     command=self._confirmar_reenvio).pack(fill="x", pady=(8, 0))

    def _confirmar_reenvio(self):
        import tkinter.messagebox as _mb
        confirmar = _mb.askyesno(
            "Imprimir novamente",
            f"Tem certeza que quer processar a Data {self.var_data.get()} "
            f"({self.setor_selecionado.get()}) de novo?\n\n"
            "Use só em caso de erro -- isso pode reimprimir pedidos que já "
            "foram impressos com sucesso antes (qualquer pedido que já não "
            "estiver mais 'NOVO' no site é pulado, mantendo o status que já "
            "tinha, então não duplica a etiqueta em si)."
        )
        if confirmar:
            self._iniciar_processamento(forcar=True)


    def _mudar_estado(self, novo, info=None):
        self.estado = novo
        self._renderizar_estado()

    def _resetar_para_nova_impressao(self):
        self._ultima_data = self.var_data.get()
        self._mudar_estado("pronto")

    def _iniciar_processamento(self, forcar=False):
        data_texto = self.var_data.get().strip()
        setor      = self.setor_selecionado.get()
        modelo     = self.modelo_selecionado.get()
        impressora = self.impressora_selecionada.get()

        try:
            data_dt = datetime.strptime(data_texto, "%d/%m/%Y")
        except Exception:
            registrar_log(["❌  Data em formato inválido. Use dd/mm/aaaa."], tag="erro")
            return

        if not forcar:
            recente, idade_min, hora_texto = _verificar_impressao_recente(setor, data_dt)
            if recente:
                self._info_recente = {
                    "data": data_texto, "setor": setor,
                    "quando": hora_texto, "minutos": int(idade_min),
                }
                self._mudar_estado("recente")
                return

        self._ultima_data = data_texto
        _parar_ciclo.clear()
        self.estado = "processando"
        self._renderizar_estado()

        threading.Thread(target=self._executar_fluxo, args=(data_texto, setor, modelo, impressora), daemon=True).start()

    def _executar_fluxo(self, data_texto, setor, modelo, impressora):
        _gerenciar_log()
        registrar_log([f"🖨️  Iniciando impressão -- Data: {data_texto} | Setor: {setor} | "
                       f"Etiqueta: {modelo} | Impressora: {impressora}"])
        try:
            resultado = processar_ciclo_impressao(data_texto, setor, modelo, impressora)
        except Exception as e:
            registrar_log([f"❌  Erro inesperado: {type(e).__name__}: {e}"], tag="erro")
            registrar_erro_permanente(f"CICLO IMPRESSÃO -- {type(e).__name__}: {e}")
            resultado = {"ok": False, "critico": False, "motivo": f"{type(e).__name__}: {e}",
                         "total": 0, "aprovados": 0, "impressos": 0, "ja_processados": 0, "erros": 0}

        self._resultado_ciclo = resultado

        if resultado["critico"]:
            self.root.after(0, lambda: self._mudar_estado("erro_critico"))
        elif not resultado["ok"]:
            self.root.after(0, lambda: self._mudar_estado("erro"))
        else:
            self.root.after(0, lambda: self._mudar_estado("concluido"))

    def _ao_fechar(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        os._exit(0)


# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
# PONTO DE ENTRADA
# ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆ ⋆⭒˚.⋆
if __name__ == "__main__":
    JanelaImpressao()
