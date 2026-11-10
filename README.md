# Análisis de precios de portátiles

Evidencia de aprendizaje sobre la extracción y el análisis de productos de la categoría de portátiles de Ktronix. El notebook contiene la metodología, las métricas, los gráficos y las conclusiones de una consulta previa. Los precios y la disponibilidad pueden cambiar.

## Ejecutar el análisis

Se requiere Python 3.12, Chrome o Chromium y acceso a internet. Desde la carpeta del repositorio:

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook Rosero_Samuel_Rico_Braian_Analizando_EA1.ipynb
```

Si no se dispone del comando `jupyter notebook`, instala Jupyter Notebook o abre el archivo en JupyterLab o Google Colab. En Colab, clona el repositorio, instala `requirements.txt` y ejecuta desde la carpeta clonada para que Python encuentre `transformaciones.py`. Selenium requiere un navegador compatible; Selenium Manager intenta obtener el controlador adecuado. Consulta las reglas de acceso del sitio antes de ejecutar la extracción. El CSV generado es local y no se añade al repositorio.

## Flujo de trabajo DevOps

1. Crear una rama para cada cambio y abrir un pull request hacia `main`.
2. GitHub Actions instala las dependencias, valida la estructura del notebook, ejecuta las pruebas de transformación y comprueba la conversión a HTML en cada push y pull request. También se puede ejecutar desde la pestaña **Actions**.
3. Revisar el pull request y sus comprobaciones antes de integrarlo. Para exigirlas, configurar la protección de `main` en GitHub; el archivo de flujo por sí solo no impide integrar cambios con fallos.
4. Cada push a `main` vuelve a ejecutar las verificaciones y, si pasan, publica el HTML en GitHub Pages. También puede lanzarse manualmente desde Actions. En **Settings → Pages → Build and deployment**, seleccionar **GitHub Actions** como fuente. La dirección esperada es https://samu975.github.io/PPanalisisDatos/ una vez completado el despliegue.

La publicación convierte las salidas guardadas en el notebook: no ejecuta la extracción ni actualiza los precios. Para actualizar el informe, ejecutar el notebook en un entorno preparado, revisar sus resultados y guardar el notebook antes de enviar el cambio. La extracción depende de la disponibilidad y estructura del sitio externo.

Para ejecutar las pruebas localmente:

```bash
python -m unittest discover -s tests -v
```
