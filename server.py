import socket
import logging
import random
import string

def run_server():
    #create socket and bind to host and port
    host = "localhost"
    port = 8050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    # listen for incoming connections
    server.listen(0)
    logging.debug(f"Listening on {server}")
    logging.debug("Waiting for incoming connections")

    conn,addr = server.accept()
    
    logging.debug(f"Connecting to {addr}")
    logging.debug("Receiving data...:")
    
    #incomming_data = ""
    while True:
        data = conn.recv(1024)

        if not data:
            break

        received_data = data.decode()
        logging.debug(f"Received data: {received_data}")

        ponderation_value = process_data(received_data)
        logging.debug(f"Ponderation value: {ponderation_value}")

        conn.send(str(ponderation_value).encode("utf-8"))

        #incomming_data = incomming_data + data.decode()

        #conn.sendall(data)

    conn.close()

"""Metodo para calcular la ponderacion de la cadena recibida"""
def process_data(data):
    
    if "aa" in data or "AA" in data or "aA" in data or "Aa" in data:
        logging.debug(f"Double 'a' rule detected >> '{data}'")
        return 1000
    
    #(Cantidad de letras * 1.5 + Cantidad de números * 2) / cantidad de espacios.
    cant_letras = 0
    cant_digits = 0
    cant_espacios = 0

    for caracter in data:
        if caracter in string.ascii_letters:
            cant_letras = cant_letras + 1
        if caracter in string.digits:
            cant_digits = cant_digits + 1
        if caracter == ' ':
            cant_espacios = cant_espacios + 1

    ponderacion = (cant_letras * 1.5 + cant_digits * 2) / cant_espacios

    return ponderacion



if __name__ == "__main__":
    #configurar el logging
    logging.basicConfig(filename='server.log', level=logging.DEBUG)

    run_server()

