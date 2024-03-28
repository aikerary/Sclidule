import requests
import json
import tabulate
import os
import textwrap

# Función para realizar la solicitud GET y obtener el JSON
def obtenerJSON(url, usuario, contrasena):
    response = requests.get(url, auth=(usuario, contrasena))
    return response.text

# Función para mostrar el horario
def mostrarHorario(usuario, contrasena, codigo):
    # Obtener el JSON de la URL correspondiente
    url = f"https://cardon.uninorte.edu.co/un-mobileserver/api/2.0/courses/overview/{codigo}"
    jsonStr = obtenerJSON(url, usuario, contrasena)

    # Analizar el JSON
    root = json.loads(jsonStr)

    # Extraer los nombres de los semestres
    semestres = [term["name"] for term in root["terms"]]

    # Solicitar al usuario que seleccione un semestre
    print("Seleccione un semestre:")
    for i, semestre in enumerate(semestres):
        print(f"{i + 1}. {semestre}")
    seleccionSemestre = int(input()) - 1

    # Obtener las secciones del semestre seleccionado
    sections = root["terms"][seleccionSemestre]["sections"]

    # Crear una matriz para almacenar la información de las clases
    horario = [["Hora", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]]

    for i in range(1, 15):
        horario.append([f"{6 + i - 1}:30-{6+i}:30", "", "", "", "", "", ""])

    # Llenar la matriz con la información de las clases
    for section in sections:
        sectionTitle = section["sectionTitle"]
        for meetingPattern in section["meetingPatterns"]:
            startTime = meetingPattern["startTime"]
            endTime=meetingPattern["endTime"]
            dayOfWeek = meetingPattern["daysOfWeek"][0]
            horaInicio = int(startTime[:2]) -10
            if endTime[:2]<="1":
                horaFin= int(endTime[:2]) + 14
            else:
                horaFin= int(endTime[:2]) -10
            columnas={1:7, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6}
            columna=columnas[dayOfWeek]
            if columna==7:
                continue
            newlist=list(x for x in range(horaInicio, horaFin))
            for hora in newlist:
                horario[hora][columna] = sectionTitle
    # Clear the console
    os.system('cls')
    # Get the width of the console
    console_width = os.get_terminal_size().columns

    # Calculate the width of each column
    column_width = console_width // 8
    # Wrap the text in each cell
    for i, row in enumerate(horario):
        for j, cell in enumerate(row):
            horario[i][j] = textwrap.fill(cell, column_width)
    # Print the table with centered alignment
    print(tabulate.tabulate(horario, headers="firstrow", tablefmt="grid"))

def main():
    # If the file credentials exist extract the credentials
    if os.path.exists("credentials.txt"):
        # Ask the user if he wants to change credentials
        # or use the ones in the file
        change = input("¿Desea cambiar las credenciales? (s/n): ")
        if change == "s":
            usuario = input("Ingrese su usuario: ")
            contrasena = input("Ingrese su contraseña: ")
            codigo = input("Ingrese su código: ")
            with open("credentials.txt", "w") as file:
                file.write(f"{usuario}\n{contrasena}\n{codigo}")
        else:
            with open("credentials.txt", "r") as file:
                credentials = file.readlines()
                usuario = credentials[0].strip()
                contrasena = credentials[1].strip()
                codigo = credentials[2].strip()
    else:
        usuario = input("Ingrese su usuario: ")
        contrasena = input("Ingrese su contraseña: ")
        codigo = input("Ingrese su código: ")
        with open("credentials.txt", "w") as file:
            file.write(f"{usuario}\n{contrasena}\n{codigo}")
    mostrarHorario(usuario, contrasena, codigo)

if __name__ == "__main__":
    main()

