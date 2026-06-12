"""
app.py — Ponto de entrada do GEO HOUSE
Roda na raiz da pasta cotokin/

Uso:
    python app.py

O que faz:
  1. Sobe o backend FastAPI na porta 8000
  2. Sobe o frontend Vue (npm run dev) na porta 5173
  3. Ctrl+C encerra os dois processos
"""

import subprocess
import sys
import os
import signal
import time

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "Back-End-FastAPI-main", "geohouse")
FRONTEND_DIR = BASE_DIR


def check_requirements():
    """Verifica dependências básicas antes de subir."""
    import shutil

    missing = []
    if not shutil.which("python3") and not shutil.which("python"):
        missing.append("Python 3")
    if not shutil.which("npm"):
        missing.append("npm (Node.js)")
    if missing:
        print(f"❌ Dependências faltando: {', '.join(missing)}")
        sys.exit(1)

    req_file = os.path.join(BACKEND_DIR, "requirements.txt")
    if os.path.exists(req_file):
        print("📦 Verificando pacotes Python...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", req_file, "-q"],
            cwd=BACKEND_DIR,
        )

    node_modules = os.path.join(FRONTEND_DIR, "node_modules")
    if not os.path.exists(node_modules):
        print("📦 Instalando dependências Node.js (primeira vez)...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR)


def main():
    check_requirements()

    procs = []

    print("\n🚀 Iniciando GEO HOUSE...\n")

    # ── Backend FastAPI ────────────────────────────────────────────────────────
    backend_cmd = [sys.executable, "main.py"]
    backend = subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    procs.append(backend)
    print(f"✅ Backend FastAPI → http://localhost:8000  (PID {backend.pid})")
    print(f"   Documentação   → http://localhost:8000/docs")

    time.sleep(1)  # aguarda backend inicializar

    # ── Frontend Vue ───────────────────────────────────────────────────────────
    frontend = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    procs.append(frontend)
    print(f"✅ Frontend Vue   → http://localhost:5173  (PID {frontend.pid})")

    print("\n📌 Pressione Ctrl+C para encerrar ambos os servidores.\n")

    # ── Aguarda e encerra os dois com Ctrl+C ───────────────────────────────────
    def shutdown(sig, frame):
        print("\n🛑 Encerrando servidores...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        for p in procs:
            p.wait()
        print("👋 GEO HOUSE encerrado.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Mantém rodando até um processo morrer ou Ctrl+C
    while True:
        for p in procs:
            if p.poll() is not None:
                print(f"⚠️  Processo (PID {p.pid}) encerrou inesperadamente.")
                shutdown(None, None)
        time.sleep(1)


if __name__ == "__main__":
    main()
