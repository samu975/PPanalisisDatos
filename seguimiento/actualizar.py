"""Consulta puntual de la categoría y genera un informe estático verificable."""
import csv
import html
import json
import re
import statistics
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from transformaciones import a_pesos, marca_desde_nombre

BASE = 'https://www.ktronix.com'
URL = BASE + '/computadores-tablets/computadores-portatiles/c/BI_104_KTRON'
TARJETA = 'li.ais-InfiniteHits-item'
NOMBRE = 'h3.product__item__top__title'
ID_HP = '199642458734'


def leer_texto(elemento, selector):
    elementos = elemento.find_elements(By.CSS_SELECTOR, selector)
    return re.sub(r'\s+', ' ', elementos[0].get_attribute('textContent')).strip() if elementos else ''


def consultar():
    opciones = webdriver.ChromeOptions()
    for parametro in ('--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--window-size=1366,900'):
        opciones.add_argument(parametro)
    navegador = webdriver.Chrome(options=opciones)
    try:
        navegador.get(URL)
        WebDriverWait(navegador, 30).until(lambda n: n.find_elements(By.CSS_SELECTOR, TARJETA + ' ' + NOMBRE))
        for _ in range(15):
            botones = navegador.find_elements(By.CSS_SELECTOR, 'button.ais-InfiniteHits-loadMore')
            if not botones or 'disabled' in (botones[0].get_attribute('class') or '') or not botones[0].is_enabled():
                break
            cantidad = len(navegador.find_elements(By.CSS_SELECTOR, TARJETA))
            navegador.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click()", botones[0])
            WebDriverWait(navegador, 25).until(lambda n: len(n.find_elements(By.CSS_SELECTOR, TARJETA)) > cantidad)
            time.sleep(3)
        else:
            raise RuntimeError('Se alcanzó el límite de cargas; no se publicará una consulta posiblemente incompleta.')
        contador = leer_texto(navegador, '.product__listing__stats')
        anunciados = re.findall(r'\d+', contador)
        if not anunciados:
            raise RuntimeError('No se encontró el contador de productos; no es posible validar cobertura.')
        productos = []
        for tarjeta in navegador.find_elements(By.CSS_SELECTOR, TARJETA):
            elementos = tarjeta.find_elements(By.CSS_SELECTOR, NOMBRE)
            if not elementos:
                raise RuntimeError('Se encontró una tarjeta sin nombre.')
            nombre = leer_texto(tarjeta, NOMBRE)
            precio = a_pesos(leer_texto(tarjeta, 'span.price'))
            codigo = elementos[0].get_attribute('data-id') or ''
            if not nombre or not precio or not codigo:
                raise RuntimeError('Se encontró un producto sin nombre, código o precio válido.')
            productos.append({'codigo': codigo, 'nombre': nombre, 'marca': marca_desde_nombre(nombre), 'precio_cop': precio})
        if not productos or len({p['codigo'] for p in productos}) != len(productos):
            raise RuntimeError('La extracción está vacía o contiene códigos duplicados.')
        total = int(anunciados[-1])
        if not total or len(productos) / total < .95:
            raise RuntimeError(f'Cobertura insuficiente: {len(productos)}/{total}.')
        return productos, total
    finally:
        navegador.quit()


def generar(productos, total, fecha):
    precios = [p['precio_cop'] for p in productos]
    marcas = Counter(p['marca'] for p in productos)
    hp = next((p for p in productos if p['codigo'] == ID_HP), None)
    dinero = lambda n: '$' + f'{n:,.0f}'.replace(',', '.')
    filas = ''.join(f"<tr><td>{html.escape(p['nombre'])}</td><td>{html.escape(p['marca'])}</td><td>{dinero(p['precio_cop'])}</td></tr>" for p in productos)
    lista = ''.join(f'<li>{html.escape(k)}: {v}</li>' for k, v in marcas.most_common())
    destacado = f"{html.escape(hp['nombre'])}: {dinero(hp['precio_cop'])}" if hp else 'El artículo destacado no apareció en esta consulta.'
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Consulta de portátiles</title><style>body{{font-family:system-ui;max-width:1000px;margin:auto;padding:2rem;color:#1c2940}}h1{{color:#143d63}}.resumen{{background:#eef5fa;padding:1rem;border-radius:8px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:.5rem;border-bottom:1px solid #ddd;text-align:left}}input{{padding:.6rem;width:85%;max-width:400px}}</style></head><body><h1>Consulta de portátiles en Ktronix</h1><p>Consulta real: {html.escape(fecha)} (hora de Colombia). Los precios pueden cambiar.</p><div class="resumen"><p>Productos: {len(productos)} de {total} anunciados.</p><p>Precio mediano: {dinero(statistics.median(precios))} COP.</p><p>Artículo destacado: {destacado}</p></div><h2>Productos por marca</h2><ul>{lista}</ul><h2>Lista de productos</h2><label for="filtro">Buscar por nombre o marca</label><p><input id="filtro" type="search" placeholder="Ejemplo: HP"></p><table><thead><tr><th>Producto</th><th>Marca</th><th>Precio (COP)</th></tr></thead><tbody>{filas}</tbody></table><script>document.querySelector('#filtro').addEventListener('input',e=>{{const q=e.target.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));}});</script></body></html>'''


def main():
    productos, total = consultar()
    fecha = datetime.now(ZoneInfo('America/Bogota'))
    carpeta = Path('datos')
    carpeta.mkdir(exist_ok=True)
    archivo = carpeta / f'ktronix_{fecha:%Y-%m-%d}.csv'
    with archivo.open('w', encoding='utf-8', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=['codigo', 'nombre', 'marca', 'precio_cop'])
        escritor.writeheader()
        escritor.writerows(productos)
    Path('dashboard.html').write_text(generar(productos, total, fecha.strftime('%Y-%m-%d %H:%M:%S')), encoding='utf-8')
    print(f'Consulta exitosa: {len(productos)}/{total}, {archivo}')

if __name__ == '__main__':
    main()
