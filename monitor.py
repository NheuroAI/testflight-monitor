import urllib.request
import sys
import datetime

URL_TESTFLIGHT = "https://testflight.apple.com/join/oscYikr0"
TEXTO_CHEIA    = "Esta versao beta esta cheia."
NTFY_URL       = "https://ntfy.sh/wabeta-9k4mX7rQ2p"

HEADERS_HTTP = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def log(msg):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{agora}] {msg}", flush=True)


def notificar_iphone(titulo, mensagem, urgente=False):
    try:
        headers = {
            "Title":    titulo,
            "Priority": "urgent" if urgente else "high",
            "Tags":     "rotating_light,iphone",
        }
        data = mensagem.encode("utf-8")
        req  = urllib.request.Request(NTFY_URL, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            log(f"Push enviado: {titulo} (status {resp.status})")
    except Exception as e:
        log(f"Erro ao enviar push: {e}")


def verificar_vaga():
    req = urllib.request.Request(URL_TESTFLIGHT, headers=HEADERS_HTTP)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    cheia = "cheia" in html.lower() or "full" in html.lower()
    return not cheia


def main():
    log("Verificando vaga no TestFlight...")
    tem_vaga = verificar_vaga()
    if tem_vaga:
        log("VAGA DETECTADA!")
        notificar_iphone(
            "VAGA NO TESTFLIGHT!",
            "WhatsApp Business beta abriu vaga! Abra agora no Safari do iPhone: testflight.apple.com/join/oscYikr0",
            urgente=True,
        )
    else:
        log("Beta ainda cheio. Nenhuma acao necessaria.")
    sys.exit(0)


if __name__ == "__main__":
    main()
