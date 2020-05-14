#1.Server socket com objeto serializado com protobuff.
import regex as re
from arvore_pb2 import  body
import ast, json
from ast import parse
from ast2json import ast2json
from google.protobuf import json_format
from google.protobuf import text_format
from collections import *
import socket, sys, struct, pickle

def transform_expression(mydict):
    mystr = ""
    for val in sorted(mydict):
        if type(mydict[val]) == type(dict()):
            if val == "left":
                pass
            elif val == 'right':
                pass
            elif val == 'op':
                pass
            mystr = mystr+transform_expression(mydict[val])
            if val == 'right':
                mystr = mystr+")"
            elif val == 'left':
                pass
            elif val == "body":
                mystr = mystr+""
        elif val == "Type" or val == "_type":
            if mydict[val] == "BinOp":
                #print("(", end='')
                mystr = mystr+"("
                pass
            elif mydict[val] in "Add Sub Div Pow Mult BitXor":
                if mydict[val] == 'Add':
                    mystr = mystr+"+"
                elif mydict[val] == 'Sub':
                    mystr = mystr+"-"
                elif mydict[val] == 'Mult':
                    mystr = mystr+"*"
                elif mydict[val] == 'Div':
                    mystr = mystr+"/"
                elif mydict[val] == 'Pow' or mydict[val] == 'BitXor':
                    mystr = mystr+"**"
            elif mydict[val] == "Num":
                mystr = mystr+str(mydict["n"])
    return mystr
        
address = ('localhost', 6005)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(address)

cout = 0
while(1):
    print ("Listening")
    message = server_socket.recv(512)
    print("mensagem", message)
    exp_buff_e = body()
    exp_buff_e.ParseFromString(message)
    mydict = json_format.MessageToDict(exp_buff_e)
    math_e = transform_expression(mydict)
    print("Calcula:", math_e,  eval(math_e))
    cout = cout+1
    print(cout)
