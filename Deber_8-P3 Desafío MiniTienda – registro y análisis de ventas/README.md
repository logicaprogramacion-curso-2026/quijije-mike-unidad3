# MiniTienda - Sistema de Registro y Análisis de Ventas

## Descripción
Sistema de consola para gestión de ventas con análisis de datos.

## Entregables (según la asignación)

1. **`MiniTienda_Mike.ipynb`** — Archivo .ipynb con el código ejecutable y las celdas
   de prueba, para abrir en Google Colab o Jupyter.
2. **`Evidencias_MiniTienda_mike.pdf`** — Documento .pdf con evidencia del desarrollo
   realizado: capturas de la ejecución (entradas/salidas), explicación breve del
   algoritmo y las respuestas a las preguntas de la asignación.
3. **`README.md`** — Este archivo, con los entregables descritos.

## Archivos de apoyo (generados por el programa)

- `minitienda.py`: código fuente equivalente al del notebook, para correr desde consola.
- `ventas.csv`: datos de ventas generados por el programa (mínimo 10 registros).
- `log.txt`: bitácora de errores e intentos fallidos (Reto D).
- `ingresos.png`: gráfico de ingresos por producto exportado con Matplotlib (Reto B).

## Requisitos cumplidos

- Catálogo con tuplas
- Precios/Stock con diccionarios
- Registro de ventas con listas
- Guardado/carga en CSV (Pandas)
- Análisis con Pandas (`groupby`) y NumPy (`mean`, `std`, `sum`)
- División por cero controlada (descuento promedio) con `try/except ZeroDivisionError`
- Gráficos con Matplotlib
- Menú interactivo con `while`, `if/elif/else`, `for`, `break`, `continue` y
  `try/except/else/finally`
- Reto A: agregar producto nuevo al catálogo
- Reto B: exportar gráfico a PNG (opción 7 del menú)
- Reto C: descuento del 5% si la cantidad es ≥ 10 unidades
- Reto D: rechazo de producto inexistente + registro del intento fallido en `log.txt`

## Cómo ejecutarlo

Abrir `MiniTienda_Mike.ipynb` en Google Colab o Jupyter y correr las celdas en orden.
Las secciones 1 a 3 definen las estructuras y funciones; la sección 4 contiene celdas de
prueba que simulan el uso del programa sin necesidad de escribir datos manualmente. Para
usar el menú interactivo con `input()`, descomentar `menu()` al final de la sección 3.

## Flujo de entrega (Git)

```
git pull
git add .
git commit -m "MiniTienda: registro y analisis de ventas"
git push
```

## Autora
Mike Quijije Chele

## Fecha
18/08/2026
