import socket
import logging
import string
import time

class Server:

    """
    Constructor de la clase server.
    """
    def __init__(self, host= "localhost", port= 8050):
        self.__host = host
        self.__port = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__host, self.__port))
    
    """
    Ejecutar el servidor para que espere conecciones.
    """
    def run_server(self):
        # listen for incoming connections
        self.__server.listen(0)
        logging.debug(f"Listening on {self.__server}")
        logging.debug("Waiting for incoming connections")

        conn,addr = self.__server.accept()
    
        logging.debug(f"Accepting incoming data from {addr}")
        logging.debug("Receiving data...:")
        
        while True:
            data = conn.recv(1024)

            if not data:
                break
            
            received_data = data.decode()
            ponderation_value = self.__process_data(received_data)

            logging.debug(f"[Received data: {received_data}, Ponderation value: {ponderation_value}]")

            conn.send(str(ponderation_value).encode("utf-8"))

        conn.close()

        return

    """
    Metodo para calcular la ponderacion de la cadena recibida.
    """
    def __process_data(self, data):
        
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
    start = time.time()
    #configurar el logging
    logging.basicConfig(filename='server.log', level=logging.DEBUG, filemode='w')

    #crear el objeto server y ejecutarlo
    server = Server(host="localhost", port=8050)
    server.run_server()
    end = time.time()
    duration = end - start
    logging.debug(f"Server Process completed in {duration} seconds.")