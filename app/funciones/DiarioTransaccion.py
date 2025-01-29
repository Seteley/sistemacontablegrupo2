from app.db_connection import obtener_conexion

def registrar_diario(fecha, glosa):
    """Registra un nuevo asiento en la tabla Diario y devuelve su ID."""
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                I   NSERT INTO Diario (Fecha, Glosa)
                VALUES (%s, %s)
                RETURNING ID_Diario
            """, (fecha, glosa))
            id_diario = cursor.fetchone()[0]
            conn.commit()
            return id_diario

def obtener_cuentas():
    """Devuelve un diccionario con las cuentas disponibles en la tabla Cuenta."""
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID_Cuenta, Nombre_Cuenta FROM Cuenta ORDER BY ID_Cuenta;")
            cuentas = cursor.fetchall()
            return {cuenta[0]: cuenta[1] for cuenta in cuentas}

def registrar_asiento_completo():
    """Flujo interactivo para registrar un asiento contable completo."""
    fecha = input("Ingrese la fecha del asiento (YYYY-MM-DD): ")
    glosa = input("Ingrese la glosa (descripción): ")

    # Registrar el asiento de diario
    id_diario = registrar_diario(fecha, glosa)
    print(f"Asiento registrado con ID: {id_diario}")

    while True:
        # Obtener las cuentas disponibles
        cuentas_disponibles = obtener_cuentas()
        print("\nCuentas disponibles:")
        for id_cuenta, nombre_cuenta in cuentas_disponibles.items():
            print(f"{id_cuenta}: {nombre_cuenta}")

        # Solicitar la selección de cuenta
        id_cuenta = int(input("Seleccione una cuenta por su ID: "))
        if id_cuenta not in cuentas_disponibles:
            print("Cuenta no válida. Intente nuevamente.")
            continue

        # Seleccionar el tipo de movimiento
        while True:
            dh = input("Indique el tipo de movimiento (Debe/Haber): ").capitalize()
            if dh in ["Debe", "Haber"]:
                break
            else:
                print("Valor inválido. Debe ser 'Debe' o 'Haber'.")

        # Ingresar el monto
        while True:
            try:
                cantidad = float(input("Ingrese el monto: "))
                if cantidad > 0:
                    break
                else:
                    print("El monto debe ser mayor a 0.")
            except ValueError:
                print("Ingrese un número válido.")

        # Preguntar si desea agregar otra transacción
        continuar = input("¿Desea agregar otra transacción a este asiento? (s/n): ").lower()
        if continuar != 's':
            break

        