# ============================================
# SISTEMA MINITIENDA - REGISTRO Y ANÁLISIS DE VENTAS
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# ============================================
# 1. CONFIGURACIÓN INICIAL (Tuplas, Diccionarios, Listas)
# ============================================


CATALOGO = (
    "Laptop Dell XPS", # ID: 0
    "Mouse Logitech", # ID: 1
    "Teclado Mecánico", # ID: 2
    "Monitor Samsung", # ID: 3
    "Audífonos Sony" # ID: 4
)


PRECIOS = {
    0: 1200.00,
    1: 45.50,
    2: 89.90,
    3: 350.00,
    4: 120.00
}

STOCK = {
    0: 10,
    1: 50,
    2: 30,
    3: 15,
    4: 25
}


ventas_buffer = []

# ============================================
# 2. FUNCIONES DEL SISTEMA
# ============================================

def mostrar_catalogo():
    """Muestra el catálogo completo con precios y stock"""
    print("\n" + "="*60)
    print(f"{'ID':^5} {'PRODUCTO':^30} {'PRECIO':^12} {'STOCK':^8}")
    print("="*60)
    for i, producto in enumerate(CATALOGO):
        if i in PRECIOS and i in STOCK:
            print(f"{i:^5} {producto:<30} ${PRECIOS[i]:>8.2f} {STOCK[i]:>8}")
    print("="*60)

def registrar_venta():
    """Registra una venta con validaciones"""
    producto_id = None
    try:
        mostrar_catalogo()
        
        producto_id = int(input("\nID del producto: "))
        
        if producto_id not in PRECIOS:
            raise ValueError(f"Producto ID {producto_id} no existe en el catálogo")
        
        cantidad = int(input("Cantidad: "))
        
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        
        # Verificar stock
        if cantidad > STOCK[producto_id]:
            raise ValueError(f"Stock insuficiente. Disponible: {STOCK[producto_id]}")
        
        precio_unitario = PRECIOS[producto_id]
        subtotal = precio_unitario * cantidad
        descuento = 0
        
        if cantidad >= 10:
            descuento = subtotal * 0.05 
            print(f"Descuento del 5% aplicado: ${descuento:.2f}")
        
        total = subtotal - descuento
        
    except ValueError as e:
        print(f"\n Error: {e}")
        # Registrar intento fallido en log (RETO D)
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR: {e}\n")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR INESPERADO: {e}\n")
    else:
        # Este bloque solo corre si no hubo ningun error arriba
        STOCK[producto_id] -= cantidad
        
        venta = {
            'producto_id': producto_id,
            'producto': CATALOGO[producto_id],
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'descuento': descuento,
            'total': total,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        ventas_buffer.append(venta)
        
        print(f"\n Venta registrada: {CATALOGO[producto_id]} x{cantidad} = ${total:.2f}")
    finally:
        # Este bloque siempre corre, haya salido bien o mal la venta
        print("Operación de registro de venta finalizada.\n")

def guardar_csv():
    """Guarda las ventas en un archivo CSV"""
    try:
        if not ventas_buffer:
            print("No hay ventas para guardar")
            return
        
        # Convertir a DataFrame
        df = pd.DataFrame(ventas_buffer)
        
        # Guardar CSV
        df.to_csv("ventas.csv", index=False, encoding='utf-8')
        print(f"Ventas guardadas en ventas.csv ({len(df)} registros)")
        
    except Exception as e:
        print(f"Error al guardar CSV: {e}")
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR CSV: {e}\n")

def cargar_csv():
    """Carga ventas desde un archivo CSV"""
    global ventas_buffer
    try:
        if not os.path.exists("ventas.csv"):
            print("Archivo ventas.csv no existe")
            return
        
        df = pd.read_csv("ventas.csv", encoding='utf-8')
        ventas_buffer = df.to_dict('records')
        print(f"Datos cargados: {len(ventas_buffer)} ventas")
        
    except FileNotFoundError:
        print("Archivo no encontrado")
    except Exception as e:
        print(f"Error al cargar CSV: {e}")
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR CARGA: {e}\n")

def analizar_ventas():
    """Analiza las ventas usando Pandas y NumPy"""
    try:
        if not ventas_buffer:
            print("No hay ventas para analizar")
            return
        
    
        df = pd.DataFrame(ventas_buffer)
        
        totales = np.array(df['total'])
        
        print("\n" + "="*60)
        print("ANÁLISIS DE VENTAS")
        print("="*60)
        print(f"Total ventas: {len(df)}")
        print(f"Total ingresos: ${np.sum(totales):.2f}")
        print(f"Ingreso promedio: ${np.mean(totales):.2f}")
        print(f"Desviación estándar: ${np.std(totales):.2f}")
        
        print("\n INGRESOS POR PRODUCTO:")
        ingresos_por_producto = df.groupby('producto')['total'].sum().sort_values(ascending=False)
        for producto, ingreso in ingresos_por_producto.items():
            print(f" {producto}: ${ingreso:.2f}")
        
        # Producto más vendido
        producto_top = df.groupby('producto')['cantidad'].sum().idxmax()
        print(f"\n Producto más vendido: {producto_top}")
        
        # Descuento promedio solo entre las ventas que SI tuvieron descuento
        # (division por cero controlada: puede que ninguna venta haya calificado)
        ventas_con_descuento = df[df['descuento'] > 0]
        try:
            promedio_descuento = float(ventas_con_descuento['descuento'].sum()) / len(ventas_con_descuento)
        except ZeroDivisionError:
            print("\n No se aplicaron descuentos en ninguna venta todavia.")
        else:
            print(f"\n Descuento promedio en ventas con descuento (>=10 u.): ${promedio_descuento:.2f}")
        
        return df, ingresos_por_producto
        
    except Exception as e:
        print(f"Error en análisis: {e}")
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR ANALISIS: {e}\n")
        return None, None

AUTOR_GRAFICO = "Sheyla Tumbaco Morán"
MATERIA_GRAFICO = "Arquitectura de Computadoras y Sistemas Operativos"


def _construir_grafico_ingresos(ingresos_por_producto):
    """Crea la figura de ingresos por producto con estilo profesional
    (barras horizontales ordenadas, etiquetas en miles, pie de autor).
    Devuelve la figura y el eje ya listos para mostrar o guardar."""
    datos_ordenados = ingresos_por_producto.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)

    colores = plt.cm.Blues(np.linspace(0.45, 0.9, len(datos_ordenados)))
    barras = ax.barh(datos_ordenados.index, datos_ordenados.values,
                      color=colores, edgecolor='#1B3A4B', linewidth=0.8, height=0.62)

    for barra, valor in zip(barras, datos_ordenados.values):
        ax.text(valor + datos_ordenados.values.max() * 0.012,
                 barra.get_y() + barra.get_height() / 2,
                 f'${valor:,.2f}', va='center', ha='left',
                 fontsize=10.5, color='#1B3A4B', fontweight='bold')

    ax.set_title('Ingresos por Producto - MiniTienda', fontsize=17,
                  fontweight='bold', color='#1B3A4B', pad=18)
    ax.set_xlabel('Ingresos ($)', fontsize=12, color='#333333', labelpad=10)
    ax.set_ylabel('')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(axis='y', labelsize=11.5, colors='#1B3A4B', length=0)
    ax.tick_params(axis='x', labelsize=10, colors='#555555')
    ax.set_xlim(0, datos_ordenados.values.max() * 1.18)
    ax.grid(axis='x', color='#E0E0E0', linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    fig.text(0.99, 0.01, f'{AUTOR_GRAFICO}  •  {MATERIA_GRAFICO}  •  {fecha_hoy}',
              ha='right', va='bottom', fontsize=8.5, color='#8A8A8A', style='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    return fig, ax


def graficar_ingresos():
    """Genera gráfica de ingresos por producto"""
    try:
        if not ventas_buffer:
            print("No hay datos para graficar")
            return

        df = pd.DataFrame(ventas_buffer)
        ingresos_por_producto = df.groupby('producto')['total'].sum()

        _construir_grafico_ingresos(ingresos_por_producto)
        plt.show()

    except Exception as e:
        print(f"Error al graficar: {e}")
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - ERROR GRAFICA: {e}\n")

def exportar_grafico_png():
    """Exporta el gráfico a PNG (RETO B)"""
    try:
        if not ventas_buffer:
            print("No hay datos para exportar")
            return

        df = pd.DataFrame(ventas_buffer)
        ingresos_por_producto = df.groupby('producto')['total'].sum()

        _construir_grafico_ingresos(ingresos_por_producto)
        plt.savefig("ingresos.png", dpi=200, bbox_inches='tight')
        print("Gráfico exportado como 'ingresos.png'")
        plt.close()

    except Exception as e:
        print(f"Error al exportar: {e}")

def agregar_producto():
    """Agrega un nuevo producto al catálogo (RETO A)"""
    try:
        print("\n" + "="*60)
        print("AGREGAR NUEVO PRODUCTO")
        print("="*60)
        
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        
        precio = float(input("Precio: $"))
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        
        stock = int(input("Stock inicial: "))
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Nuevo ID
        nuevo_id = max(PRECIOS.keys()) + 1
        
        # Actualizar estructuras
        global CATALOGO
        CATALOGO = CATALOGO + (nombre,)
        PRECIOS[nuevo_id] = precio
        STOCK[nuevo_id] = stock
        
        print(f"Producto agregado: ID {nuevo_id} - {nombre}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def generar_datos_ejemplo():
    """Genera datos de ejemplo para pruebas"""
    print("Generando datos de ejemplo...")
    productos_ejemplo = [
        (0, 2), (0, 1), (1, 5), (2, 3), 
        (3, 1), (4, 2), (1, 3), (2, 4),
        (0, 1), (3, 2)
    ]
    
    for prod_id, cant in productos_ejemplo:
        try:
            # Simular venta sin restar stock real
            venta = {
                'producto_id': prod_id,
                'producto': CATALOGO[prod_id],
                'cantidad': cant,
                'precio_unitario': PRECIOS[prod_id],
                'descuento': 0 if cant < 10 else PRECIOS[prod_id]*cant*0.05,
                'total': PRECIOS[prod_id]*cant * (0.95 if cant >= 10 else 1),
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            ventas_buffer.append(venta)
        except:
            pass
    
    print(f"{len(ventas_buffer)} ventas generadas")

# ============================================
# 3. MENÚ PRINCIPAL
# ============================================

def menu():
    """Menú principal del sistema"""
    while True:
        print("\n" + "="*60)
        print("MINITIENDA - SISTEMA DE VENTAS")
        print("="*60)
        print("1) Ver catálogo")
        print("2) Registrar venta")
        print("3) Guardar ventas (CSV)")
        print("4) Cargar ventas (CSV)")
        print("5) Analizar ventas")
        print("6) Mostrar gráfica")
        print("7) Exportar gráfica a PNG (RETO B)")
        print("8) Agregar producto (RETO A)")
        print("9) Generar datos de ejemplo")
        print("0) Salir")
        print("="*60)
        
        try:
            opcion = input("Seleccione una opción: ").strip()
            
            if not opcion:
                continue
                
            opcion = int(opcion)
            
            if opcion == 1:
                mostrar_catalogo()
                
            elif opcion == 2:
                registrar_venta()
                
            elif opcion == 3:
                guardar_csv()
                
            elif opcion == 4:
                cargar_csv()
                
            elif opcion == 5:
                analizar_ventas()
                
            elif opcion == 6:
                graficar_ingresos()
                
            elif opcion == 7:
                exportar_grafico_png()
                
            elif opcion == 8:
                agregar_producto()
                
            elif opcion == 9:
                generar_datos_ejemplo()
                
            elif opcion == 0:
                print("\n¡Gracias por usar MiniTienda!")
                break
                
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Por favor, ingrese un número válido")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")
            with open("log.txt", "a") as log_file:
                log_file.write(f"{datetime.now()} - ERROR MENU: {e}\n")

# ============================================
# 4. EJECUCIÓN PRINCIPAL
# ============================================

if __name__ == "__main__":
    print("Bienvenido a MiniTienda")
    menu()
