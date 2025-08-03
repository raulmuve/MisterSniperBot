import re

def convertir_a_nombre_completo(nombre: str, link: str) -> str:
    # Si el nombre no es del tipo 'X. Apellido', no tocamos nada
    if not re.match(r"^[A-Z]\.[ \xa0][A-Z]", nombre):
        return nombre.strip()

    # Extraer el slug del link, tipo: 'players/29/inaki-williams'
    try:
        slug = link.split('/')[-1]  # 'inaki-williams'
        partes = slug.split('-')
        if len(partes) < 2:
            return nombre.strip()
        nombre_completo = ' '.join([p.capitalize() for p in partes])
        return nombre_completo.strip()
    except Exception:
        return nombre.strip()
