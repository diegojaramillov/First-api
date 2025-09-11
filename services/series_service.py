# services/series_service.py
# Aquí va la lógica que maneja los datos (crear, leer, actualizar, eliminar).
# Separar la lógica en "services" ayuda a que los controladores (rutas) sean simples.

from data.data import comedy_series

def get_all():
    # Devuelve todas las series (referencia directa a la lista en memoria)
    return comedy_series

def get_by_id(series_id: int):
    # Busca una serie por su id; devuelve None si no existe
    return next((s for s in comedy_series if s["id"] == series_id), None)

def title_exists(title: str):
    # Comprueba si ya existe una serie con ese título (case-insensitive)
    return any(s for s in comedy_series if s["title"].lower() == title.lower())

def create_series(data: dict):
    # Crea una nueva serie con id autoincremental
    new_id = max((s["id"] for s in comedy_series), default=0) + 1
    series = {
        "id": new_id,
        "title": data["title"],
        "seasons": data.get("seasons", 1),
        "platform": data.get("platform", "Desconocida")
    }
    comedy_series.append(series)
    return series

def update_series(series_id: int, data: dict):
    # Actualiza campos existentes de una serie
    series = get_by_id(series_id)
    if not series:
        return None
    series["title"] = data.get("title", series["title"])
    series["seasons"] = data.get("seasons", series["seasons"])
    series["platform"] = data.get("platform", series["platform"])
    return series

def delete_series(series_id: int):
    # Elimina una serie por id
    series = get_by_id(series_id)
    if not series:
        return False
    comedy_series.remove(series)
    return True

def stats_by_platform():
    # Devuelve conteo de series por plataforma
    stats = {}
    for s in comedy_series:
        p = s.get("platform", "Desconocida")
        stats[p] = stats.get(p, 0) + 1
    return stats
