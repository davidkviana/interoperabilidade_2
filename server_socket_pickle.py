#3.Server Socket com objeto serializado com pickle sem o protobuff.
import compress_pickle as pickle
import json, socket, astor
        
address = ('localhost', 6005)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(address)

while(1):
    print ("Listening")
    message = server_socket.recv(512)
    deserialize = pickle.loads(message, compression="gzip")
    math_e = astor.to_source(deserialize).replace('\n', '')
    print("Calcula", math_e, "=", eval(math_e))
    
