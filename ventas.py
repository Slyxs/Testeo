import pandas as pd
from datetime import datetime

# Cargar los productos desde el archivo CSV usando pandas
def cargar_productos():
    try:
        productos = pd.read_csv('Productos.csv', encoding='utf-8')
        productos.set_index('ID', inplace=True)  # Usar la columna 'ID' como índice
        return productos
    except FileNotFoundError:
        print("Error: El archivo 'Productos.csv' no se encontró.")
        return None

# Mostrar el menú de opciones
def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Realizar compra")
    print("2. Imprimir boleta")
    print("3. Salir")
    print("4. Ver historial de ventas")
    print("5. Exportar historial de ventas a Excel")

# Realizar una compra
def realizar_compra(productos):
    compra = []
    while True:
        try:
            id_producto = int(input("Ingrese el ID del producto (0 para terminar): "))
            if id_producto == 0:
                break
            if id_producto not in productos.index:
                print("ID de producto no válido. Intente de nuevo.")
                continue
            producto = productos.loc[id_producto]
            print(f"Producto seleccionado: {producto['Nombre']} (Stock: {producto['Stock']})")
            cantidad = int(input("Ingrese la cantidad: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que 0.")
                continue
            if cantidad > producto['Stock']:
                print(f"No hay suficiente stock. Stock disponible: {producto['Stock']}")
                continue
            compra.append((id_producto, cantidad))
            print("Producto añadido a la compra.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")
    return compra

# Guardar la venta en el historial
def guardar_venta(nombre_cliente, dni_cliente, compra, productos):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(productos.loc[id_producto]['Precio unitario'] * cantidad for id_producto, cantidad in compra)
    
    # Crear una lista con los detalles de la venta
    detalles_venta = []
    for id_producto, cantidad in compra:
        producto = productos.loc[id_producto]
        detalles_venta.append({
            'Fecha': fecha,
            'Cliente': nombre_cliente,
            'DNI': dni_cliente,
            'Producto': producto['Nombre'],
            'Cantidad': cantidad,
            'Precio Unitario': producto['Precio unitario'],
            'Subtotal': producto['Precio unitario'] * cantidad
        })
    
    # Guardar en el archivo CSV
    try:
        df = pd.DataFrame(detalles_venta)
        df.to_csv('historial_ventas.csv', mode='a', index=False, header=not pd.io.common.file_exists('historial_ventas.csv'))
        print("Venta guardada en el historial.")
    except Exception as e:
        print(f"Error al guardar la venta: {e}")

# Imprimir la boleta
def imprimir_boleta(productos, compra):
    if not compra:
        print("No hay productos en la compra.")
        return

    nombre_cliente = input("Ingrese el nombre del cliente: ")
    dni_cliente = input("Ingrese el DNI del cliente: ")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n--- Boleta ---")
    print(f"Fecha: {fecha}")
    print(f"Cliente: {nombre_cliente}")
    print(f"DNI: {dni_cliente}")
    print("\nProductos:")

    total = 0
    for id_producto, cantidad in compra:
        producto = productos.loc[id_producto]
        subtotal = producto['Precio unitario'] * cantidad
        total += subtotal
        print(f"{producto['Nombre']} x {cantidad} = ${subtotal:.2f}")

    print(f"\nTotal a pagar: ${total:.2f}")

    try:
        pago = float(input("Ingrese con cuánto paga el cliente: "))
        if pago < total:
            print("El pago es insuficiente.")
        else:
            vuelto = pago - total
            print(f"Vuelto: ${vuelto:.2f}")
    except ValueError:
        print("Entrada no válida. No se pudo calcular el vuelto.")

    # Guardar la venta en el historial
    guardar_venta(nombre_cliente, dni_cliente, compra, productos)

# Ver historial de ventas
def ver_historial_ventas():
    try:
        historial = pd.read_csv('historial_ventas.csv')
        print("\n--- Historial de Ventas ---")
        print(historial)
    except FileNotFoundError:
        print("No hay historial de ventas disponible.")
    except Exception as e:
        print(f"Error al leer el historial de ventas: {e}")

# Exportar historial de ventas a Excel
def exportar_historial_a_excel():
    try:
        historial = pd.read_csv('historial_ventas.csv')
        archivo_excel = 'historial_ventas.xlsx'
        historial.to_excel(archivo_excel, index=False)
        print(f"Historial de ventas exportado exitosamente a {archivo_excel}")
    except FileNotFoundError:
        print("No hay historial de ventas disponible.")
    except Exception as e:
        print(f"Error al exportar el historial de ventas: {e}")

# Función principal
def main():
    productos = cargar_productos()
    if productos is None:
        return  # Salir si no se pudo cargar el archivo

    compra = []

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            compra = realizar_compra(productos)
        elif opcion == '2':
            imprimir_boleta(productos, compra)
        elif opcion == '3':
            print("Saliendo del sistema...")
            break
        elif opcion == '4':
            ver_historial_ventas()
        elif opcion == '5':
            exportar_historial_a_excel()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()