import socket
import sys
import random
import string
import logging
import time

"""Client class"""
class Client:
    
    """Constructor de la clase. 
    - host=127.0.0.1  IP del servidor socket
    - port=8050 Puerto en el servidor socket
    - size=100  Cantidad de cadenas
    """
    def __init__(self, host = "127.0.0.1", port = 8050, size=100) -> None:
        self.__host = host
        self.__port = port
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__size = size

    """
    Ejecutar el servidor cliente con toda la logica
    """
    def execute_client(self)->None:
        #generar archivo con las cadenas
        file = self.__generate_file()
        self.__client.connect((self.__host, self.__port))
        
        #cargar los datos del archivo con las cadenas y enviarlas el servidor para ser ponderadas
        with open(file, 'r') as file:
            content = file.readlines()
        
        data = {}

        logging.debug("Sending chains to server socket for ponderations")
        for line in content:
            line = line[:-1] # eliminando el salto de linea
            #send data to socket server
            self.__client.send(line.encode('utf-8'))
            #receive data
            received_data = self.__client.recv(1024)

            data[line] = received_data.decode()

        #cerrar la conexion al servidor
        self.__client.close()

        #salvar la informacion en un archivo
        self.__save_info_to_file(data),

    """
    Metodo para generar el archivo de las cadenas
    """
    def __generate_file(self, filename="chains.txt")-> str:
        logging.debug("Generating chains file...")
        with open(filename,'w') as file:
            for _ in range(self.__size):
                string_generado = self.__generate_string()
                file.write(string_generado + "\n")
        
        return filename
    
    """
    Funcion para generar la cadena que se debe enviar al servidor para ser ponderada.
    """
    def __generate_string(self):
        
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
    
    """
    Function for save received info to file
    """
    def __save_info_to_file(self, data, filename="chains_ponderations.txt"):

        logging.debug('Saving ponderation info to file: %s' % filename)

        with open(filename, 'w+') as file:
            for key, value in data.items():
                file.write(f"Ponderation: ({key},{value})\n")


if __name__ == "__main__":

    start = time.time()

    #configurar el logging 
    logging.basicConfig(filename='client.log', level=logging.DEBUG)

    #comprobar si se paso el tamanno de la cadena a ser generada
    argumentos = sys.argv
    if len(argumentos) > 1:
        size = int(argumentos[1])
    else:
        size = 1000000 #1000000
          
    client = Client(host="127.0.0.1", port=8050, size=size)
    client.execute_client()

    end = time.time()

    logging.debug(f"Client Process completed in {end-start} seconds.")