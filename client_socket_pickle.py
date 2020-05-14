#3.Cliente Socket com objeto serializado com pickle sem o protobuff.
import ast, json, socket, sys, struct
from ast2json import ast2json
import compress_pickle as pickle

address = ('localhost', 6005) #endereco do servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #parametros do socket
client_socket.connect(address) #conectar ao servidor
list_expr = ["(25+8)+(9*7)/(32/8)**2", "(15-8)*3", "(5+9)*(3**2)", "15+15+15+15*3", "2*2*2*2*2+32", "9*9*9", "(1+2)*(3/4)"] 
for expressao in list_expr:
    expre_str_m = expressao #Recebe a exrpessao
    ast_parse_x = ast.parse(expre_str_m, "", "eval") #Cria o objeto ast – arvore binaria com a expressao
    sout = pickle.dumps(ast_parse_x, compression="gzip") #Serializa com compressao dos dados
    client_socket.sendall(sout) #Envia os dados serializados
    print("Expressao", expressao)  #imprime a expressao
