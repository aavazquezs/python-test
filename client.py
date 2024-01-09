import socket
import sys
import random
import string
import logging
from pprint import pprint

"""Funcion para enviar la informacion al servidor socket. Retorna el valor de ponderacion de la cadena enviada al servidor"""
def run_client(file):
    #configurar la conexion al servidor
    host = "127.0.0.1"
    port = 8050
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    #cargar los datos del archivo con las cadenas y enviarlas el servidor para ser ponderadas
    with open(file, 'r') as file:
        content = file.readlines()
    
    data = {}

    logging.debug("Sending chains to server socket for ponderations")
    for line in content:
        line = line[:-1] # eliminando el salto de linea
        #send data to socket server
        client.send(line.encode('utf-8'))
        #receive data
        received_data = client.recv(1024)

        data[line] = received_data.decode()

    #cerrar la conexion al servidor
    client.close()

    #salvar la informacion en un archivo
    save_info_to_file(data)

"""Genera el archivo con las cadenas generadas"""
def generate_file(size, filename="chains.txt"):

    logging.debug("Generating chains file...")

    with open(filename,'w') as file:
        for _ in range(size):
            string_generado = generate_string()
            file.write(string_generado + "\n")
    
    return filename


"""Funcion para generar la cadena que se debe enviar al servidor para ser ponderada."""
def generate_string():
    
    size = random.randint(50, 100)
    caracteres_digitos = string.ascii_letters + string.digits
    
    result = random.choice(caracteres_digitos)
    for _ in range(size):
        result = result + random.choice(caracteres_digitos)
    
    cant = random.randint(3,5)
    generated_pos = []


    for _ in range(cant):
        pos = random.randint(1, len(result)-2)
        
        while pos in generated_pos or pos - 1 in generated_pos or pos + 1 in generated_pos:
            pos = random.randint(1, len(result)-2)
        generated_pos.append(pos)

        result = result[:pos] + ' ' + result[pos+1:]

    return result

"""Function for save received info to file"""
def save_info_to_file(data, filename="chains_ponderations.txt"):

    logging.debug('Saving ponderation info to file: %s' % filename)

    with open(filename, 'w+') as file:
        for key, value in data.items():
            file.write(f"Ponderation: ({key},{value})\n")

    


if __name__ == "__main__":
    #configurar el logging 
    logging.basicConfig(filename='client.log', level=logging.DEBUG)

    #comprobar si se paso el tamanno de la cadena a ser generada
    argumentos = sys.argv
    if len(argumentos) > 1:
        size = int(argumentos[1])
    else:
        size = 100 #1000000
    
    #generar archivo con las cadenas
    file = generate_file(size)

    #conectar con el servidor socket
    ponderation_value = run_client(file)