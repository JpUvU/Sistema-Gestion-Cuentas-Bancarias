import json

ARCHIVO_DATOS = "base_de_datos.json"
base_de_datos = {}

def guardar_datos(data):
    """Guarda la información en un archivo JSON"""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def cargar_datos():
    """Carga la información desde un archivo JSON"""
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
