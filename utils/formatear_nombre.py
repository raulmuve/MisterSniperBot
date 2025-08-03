# utils/formatear_nombre.py
import re

def normalizar_nombre(nombre_abreviado: str, link: str) -> str:
    """
    Si el nombre_abreviado tiene forma 'X. Apellido', intenta obtener el nombre completo del link.
    Devuelve nombre formateado (capitalizado) o el original si no se puede mejorar.
    """
    if re.match(r"^[A-Z]\.\s", nombre_abreviado) and "players/" in link:
        partes = link.split("/")
        if len(partes) >= 3:
            nombre_raw = partes[2]  # nombre-apellido
            nombre_partes = nombre_raw.split("-")
            if len(nombre_partes) >= 2:
                nombre = nombre_partes[0].capitalize()
                apellido = " ".join(p.capitalize() for p in nombre_partes[1:])
                return f"{nombre} {apellido}"
    return nombre_abreviado.strip()
