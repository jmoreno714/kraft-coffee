"""
Deploy landing page to GitHub Pages.
Reads credentials from .env, creates the repo if needed, pushes all files,
and enables GitHub Pages on the main branch.
"""

import os
import subprocess
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

TOKEN    = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")
REPO     = os.getenv("GITHUB_REPO")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def run(cmd, **kwargs):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, **kwargs)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


def create_repo():
    print(f"[1/3] Verificando repositorio '{REPO}'...")
    r = requests.get(f"https://api.github.com/repos/{USERNAME}/{REPO}", headers=HEADERS)
    if r.status_code == 200:
        print("  Repositorio ya existe.")
        return

    print("  Creando repositorio...")
    r = requests.post(
        "https://api.github.com/user/repos",
        headers=HEADERS,
        json={"name": REPO, "private": False, "auto_init": False},
    )
    if r.status_code not in (200, 201):
        print(f"ERROR al crear repo: {r.json()}")
        sys.exit(1)
    print("  Repositorio creado.")


def push_files():
    print("[2/3] Configurando git y haciendo push...")
    remote_url = f"https://{TOKEN}@github.com/{USERNAME}/{REPO}.git"

    git_dir = ROOT / ".git"
    if not git_dir.exists():
        run(["git", "init", "-b", "main"])
    else:
        # ensure we're on main
        subprocess.run(["git", "checkout", "-B", "main"], capture_output=True, cwd=ROOT)

    # configure remote
    remotes = run(["git", "remote"])
    if "origin" in remotes:
        run(["git", "remote", "set-url", "origin", remote_url])
    else:
        run(["git", "remote", "add", "origin", remote_url])

    run(["git", "config", "user.email", "deploy@kraft-coffee.com"])
    run(["git", "config", "user.name",  "Kraft Deploy"])

    print("  Commiteando archivos...")
    run(["git", "add", "index.html", "brand_assets", ".gitignore", "workflows", "tools", "CLAUDE.md"])

    # check if there's anything to commit
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=ROOT)
    if status.stdout.strip():
        run(["git", "commit", "-m", "deploy: Kraft Coffee landing page"])
    else:
        print("  Sin cambios nuevos, forzando push...")

    print("  Haciendo push a GitHub...")
    run(["git", "push", "-u", "origin", "main", "--force"])
    print("  Push completado.")


def enable_pages():
    print("[3/3] Activando GitHub Pages...")
    r = requests.post(
        f"https://api.github.com/repos/{USERNAME}/{REPO}/pages",
        headers=HEADERS,
        json={"build_type": "legacy", "source": {"branch": "main", "path": "/"}},
    )
    if r.status_code in (200, 201, 204):
        print("  GitHub Pages activado.")
    elif r.status_code == 409:
        print("  GitHub Pages ya estaba activado.")
    else:
        print(f"  Advertencia al activar Pages: {r.status_code} — {r.json()}")


def main():
    if not all([TOKEN, USERNAME, REPO]):
        print("ERROR: Faltan variables en .env (GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO)")
        sys.exit(1)

    create_repo()
    push_files()
    enable_pages()

    url = f"https://{USERNAME}.github.io/{REPO}/"
    print()
    print("=" * 50)
    print(f"  DEPLOY COMPLETO")
    print(f"  URL: {url}")
    print(f"  (puede tardar 1-2 minutos en activarse)")
    print("=" * 50)


if __name__ == "__main__":
    main()
