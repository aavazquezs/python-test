import socket
import logging

def run_server():
    #create socket and bind to host and port
    host = "localhost"
    port = 8050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server}")

    print("Waiting for incoming connections")
    conn,addr = server.accept()
    print(f"Connecting to {addr}")

    print("Received data:")
    incomming_data = ""
    while True:
        data = conn.recv(1024)

        print(data)

        if not data:
            break

        incomming_data = incomming_data + data.decode()
        conn.sendall(data)

    print(incomming_data)

    conn.close()


def process_data(data):
    logging.basicConfig(filename='server.log', level=logging.DEBUG)
    logging.debug('This message should be logged in the file')



if __name__ == "__main__":
    run_server()

