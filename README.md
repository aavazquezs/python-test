# Avangenio Python Test

## Installation and use guide:

1 - Install python 3 on your system. For linux platforms use the command below:
    
    sudo apt install python3

This solution only uses Python 3 built-in libraries

2 - Copy the files **client.py** and **server.py** to your computer file system

3 - First, execute the server script using the following command:

    python3 server.py

4 - Second, execute the client script using the following command:

    python3 client.py <chain_number> <host> <port>

You can set the number of chains to generate, the default value is 1 000 000 chains. Also you can set the host and port, the default values are "127.0.0.1" and 8050.

The result will be saved in the files **chains_ponderations.txt**