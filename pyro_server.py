#3.Server Pyro(RMI) com objeto serializado com pickle.
import sys
import Pyro4
from Pyro4.util import *
import ast 
import serpent
import astor
import pickle
import base64

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Expression(object):
        def __init__(self):
            self.expr = None

        def set_expression(self, expr):
            dec = base64.b64decode(expr['data'])
            deserialize = pickle.loads(dec)
            rec_expr = astor.to_source(deserialize)
            self.expr = rec_expr

        def result(self):
                result = eval(self.expr)
                print("Expr:", self.expr, "result:", result)
                return result
def main():
    Pyro4.Daemon.serveSimple(
            {
                Expression: "david.Expression"
            },
            host = "192.168.1.110",
            port = 35554,
            ns = False)

if __name__=="__main__":
    main()
