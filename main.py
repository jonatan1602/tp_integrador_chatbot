import csv

ESTADO_INICIO = "INICIO"
ESTADO_DATOS = "ESPERANDO_DATOS"
ESTADO_CATEGORIA = "SELECCIONANDO_CATEGORIA"
ESTADO_SOLUCION = "CONSULTANDO_SOLUCION"
ESTADO_CONFIRMACION = "ESPERANDO_CONFIRMACION"
ESTADO_TICKET = "GENERANDO_TICKET"
ESTADO_ESCALAMIENTO = "ESCALANDO"
ESTADO_FINAL = "FINALIZADO"

def cargar_usuarios():
    usuarios = []

    with open("usuarios.csv", "r", encoding="latin-1") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")

        for fila in lector:
            usuarios.append(fila)

    return usuarios


def cargar_soluciones():
    soluciones = {}

    with open("soluciones.csv", "r", encoding="latin-1") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")

        for fila in lector:
            soluciones[fila["categoria"]] = fila["solucion"]

    return soluciones

def validar_usuario(usuarios):

    while True:

        usuario_ingresado = input(
            "Ingrese usuario del campus: "
        )

        legajo_ingresado = input(
            "Ingrese legajo: "
        )

        for usuario in usuarios:

            if (
                usuario["usuario_campus"]
                == usuario_ingresado
                and
                usuario["legajo"]
                == legajo_ingresado
            ):

                print(
                    "\nDatos validados correctamente"
                )

                return usuario

        print(
            "\nDatos incorrectos. Intente nuevamente."
        )

def seleccionar_categoria():

    categorias = [
        "Recuperacion contraseña",
        "Campus caido",
        "Problemas login",
        "Problemas tareas",
        "Inscripciones"
    ]

    while True:

        print("\nCategorias disponibles:")

        for i, categoria in enumerate(
            categorias,
            start=1
        ):

            print(
                f"{i}. {categoria}"
            )

        opcion = input(
            "\nSeleccione una opcion: "
        )

        if opcion.isdigit():

            opcion = int(opcion)

            if 1 <= opcion <= len(categorias):

                return categorias[
                    opcion - 1
                ]

        print(
            "\nOpcion invalida. Intente nuevamente."
        )

def buscar_solucion(categoria, soluciones):

    if categoria in soluciones:

        return soluciones[categoria]

    return None

def confirmar_resolucion():

    respuesta = input("\n¿El problema fue resuelto? (si/no): ").lower()

    if respuesta == "si":

        return True

    return False

def generar_ticket(usuario, categoria):

    ticket_id = 1000

    with open(
        "tickets.csv",
        "r",
        encoding="latin-1"
    ) as archivo:

        lineas = archivo.readlines()

        if len(lineas) > 1:

            ultimo_ticket = lineas[-1].strip().split(";")

            ticket_id = int(
                ultimo_ticket[0]
            ) + 1

    with open(
        "tickets.csv",
        "a",
        newline="",
        encoding="latin-1"
    ) as archivo:

        escritor = csv.writer(
            archivo,
            delimiter=";"
        )

        escritor.writerow([
            ticket_id,
            usuario["usuario_campus"],
            categoria,
            "Pendiente"
        ])

    print(
        f"\nTicket generado correctamente. ID: {ticket_id}"
    )

estado_actual = ESTADO_INICIO
usuarios = cargar_usuarios()
soluciones = cargar_soluciones()

datos_sesion = {"usuario": None, "categoria": None, "estado": estado_actual}

while estado_actual != ESTADO_FINAL:

    datos_sesion["estado"] = estado_actual

    print("\nEstado actual:", estado_actual)

    if estado_actual == ESTADO_INICIO:

        estado_actual = ESTADO_DATOS


    elif estado_actual == ESTADO_DATOS:

        usuario_valido = validar_usuario(
            usuarios
        )

        datos_sesion["usuario"] = usuario_valido

        estado_actual = ESTADO_CATEGORIA


    elif estado_actual == ESTADO_CATEGORIA:

        categoria = seleccionar_categoria()

        datos_sesion["categoria"] = categoria

        estado_actual = ESTADO_SOLUCION


    elif estado_actual == ESTADO_SOLUCION:

        solucion = buscar_solucion(
            categoria,
            soluciones
        )

        if solucion:

            print("\nSolucion encontrada:")
            print(solucion)

            estado_actual = ESTADO_CONFIRMACION

        else:

            estado_actual = ESTADO_TICKET


    elif estado_actual == ESTADO_CONFIRMACION:

        if confirmar_resolucion():

            estado_actual = ESTADO_FINAL

        else:

            estado_actual = ESTADO_TICKET


    elif estado_actual == ESTADO_TICKET:

        generar_ticket(
            usuario_valido,
            categoria
        )

        estado_actual = ESTADO_ESCALAMIENTO


    elif estado_actual == ESTADO_ESCALAMIENTO:

        print(
            "\nIncidencia escalada a soporte humano"
        )

        estado_actual = ESTADO_FINAL

print("\nProceso finalizado")