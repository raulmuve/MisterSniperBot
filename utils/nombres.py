# utils/nombres.py

def normalizar_nombre(nombre_raw: str, link: str) -> str:
    # Si el nombre ya es completo, lo dejamos tal cual
    if " " in nombre_raw and "." not in nombre_raw.split(" ")[0]:
        return nombre_raw.strip().title()

    # Si empieza con inicial tipo "D. Suárez", lo sacamos del link
    try:
        slug = link.split("/")[-1]  # ej. "david-lopez"
        partes = slug.split("-")
        if len(partes) >= 2:
            nombre = partes[0].capitalize()
            apellido = " ".join(p.capitalize() for p in partes[1:])
            return f"{nombre} {apellido}"
    except Exception:
        pass

    return nombre_raw.strip().title()
