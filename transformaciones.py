"""Funciones de limpieza para el análisis de portátiles."""
import re

MARCAS = ["LENOVO", "ASUS", "HP", "ACER", "MSI", "DELL", "SAMSUNG", "HUAWEI", "GIGABYTE", "MICROSOFT"]
ALIAS = {"MACBOOK": "APPLE", "OMNIBOOK": "HP"}


def a_pesos(valor):
    digitos = re.sub(r"\D", "", valor or "")
    return int(digitos) if digitos else None


def a_porcentaje(valor):
    hallado = re.search(r"(\d+)\s*%", valor or "")
    return int(hallado.group(1)) if hallado else 0


def marca_desde_nombre(nombre):
    palabras = re.findall(r"[A-Za-z]+", (nombre or "").upper())
    for palabra in palabras:
        if palabra in MARCAS:
            return palabra
        if palabra in ALIAS:
            return ALIAS[palabra]
    return "OTRA"
