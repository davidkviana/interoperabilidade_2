#2.Cliente Pyro(RMI) com objeto serializado com pickle.
import sys
import Pyro4
from Pyro4.util import *
import ast 
import serpent
import astor
import json
import ast2json
import pickle
import base64


#sys.excepthook = Pyro4.util.excepthook
uri = "PYRO:david.Expression@192.168.1.110:35554"
Exp = Pyro4.Proxy(uri)

list_expr = ["(25+8)+(9*7)/(32/8)**2", "(15-8)*3", "(5+9)*(3**2)", "15+15+15+15*3", "2*2*2*2*2+32", "9*9*9", "(1+2)*(3/4)"]
for n in list_expr:
    str_expr = n
    expr = ast.parse(str_expr, "", "eval")
    serialize = pickle.dumps(expr)
    Exp.set_expression(serialize)
    e = Exp.result()
    print(n, "=", e)
