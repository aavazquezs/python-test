import socket
import logging
import random

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
    return random.randint(0,len(data))



if __name__ == "__main__":
    #configurar el logging
    logging.basicConfig(filename='server.log', level=logging.DEBUG)

    run_server()

