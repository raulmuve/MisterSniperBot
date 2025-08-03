import os
from pathlib import Path

SESSION_DIR = Path("session")
SESSION_FILE = SESSION_DIR / "session.json"

def get_storage_state_path() -> str:
    """
    Devuelve la ruta absoluta al archivo de sesión para el storage_state de Playwright.
    """
    return str(SESSION_FILE.resolve())

def session_file_exists() -> bool:
    """
    Verifica si el archivo de sesión existe.
    """
    return SESSION_FILE.exists()

def save_storage_state(context) -> None:
    """
    Guarda el estado de sesión (cookies y localStorage) tras un login exitoso.
    """
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=get_storage_state_path())
