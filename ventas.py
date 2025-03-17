import csv
from datetime import datetime

# Cargar los productos desde el archivo CSV
def cargar_productos():
    productos = {}
    with open('Productos.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            productos[int(row['ID'])] = {
                'nombre': row['Nombre'],
                'precio': float(row['Precio unitario']),
                'stock': int(row['Stock']),
                'marca': row['Marca'],
                'categoria': row['Categoria'],
                'descripcion': row['Descripcion']
            }
    return productos

# Mostrar el menú de opciones
def mostrar_menu():
    print("\n--- Menú ---")
    print("1. Realizar compra")
    print("2. Imprimir boleta")
    print("3. Salir")

# Realizar una compra
def realizar_compra(productos):
    compra = []
    while True:
        try:
            id_producto = int(input("Ingrese el ID del producto (0 para terminar): "))
            if id_producto == 0:
                break
            if id_producto not in productos:
                print("ID de producto no válido. Intente de nuevo.")
                continue
            producto = productos[id_producto]
            print(f"Producto seleccionado: {producto['nombre']} (Stock: {producto['stock']})")
            cantidad = int(input("Ingrese la cantidad: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que 0.")
                continue
            if cantidad > producto['stock']:
                print(f"No hay suficiente stock. Stock disponible: {producto['stock']}")
                continue
            compra.append((id_producto, cantidad))
            print("Producto añadido a la compra.")
        except ValueError:
            print("Entrada no válida. Intente de nuevo.")
    return compra

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
        producto = productos[id_producto]
        subtotal = producto['precio'] * cantidad
        total += subtotal
        print(f"{producto['nombre']} x {cantidad} = ${subtotal:.2f}")

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

# Función principal
def main():
    productos = cargar_productos()
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
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()