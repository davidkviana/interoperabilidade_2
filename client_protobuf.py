#1.Cliente socket com objeto serializado com protobuff.
from arvore_pb2 import  body
import ast, json, socket, sys, struct
from ast import parse
from ast2json import ast2json
from google.protobuf import json_format
from google.protobuf import text_format
import pickle

address = ('localhost', 6005)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(address)

list_expr = ["(25+8)+(9*7)/(32/8)^2", "(15-8)*3", "(5+9)*(3^2)", "15+15+15+15*3", "2*2*2*2*2+32", "9*9*9", "(1+2)*(3/4)"]

for expressao in list_expr:
    expre_str_m = expressao #expressao
    ast_parse_x = ast.parse(expre_str_m, "", "eval") #objeto ast em arvore que valida as exressoes
    ast_json = ast2json(parse(ast_parse_x)) #criando o json a partir de ast
    ast_json_dump_y = json.dumps(ast_json, indent=1) #criando um dump a partir do json, porque eh string e nao json.
    exp_buff_e = body() #usando o body doprotobuff
    msg = json_format.Parse(ast_json_dump_y, exp_buff_e) #transfere os dados do ast_json para o protobuff
    s = exp_buff_e.SerializeToString() #recebendo a string de dados em protobuff - serializacao
    client_socket.sendall(s) #envia por socket o objeto serializado
