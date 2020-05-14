# interoperabilidade_2
Clientes e servidores da prática de SD.

1. Socket e protobuf.

Utilizei a linguagem python juntamente com protobuff. Contudo, tentando utilizar um módulo python chamado ast, que cria árvores a partir dessa biblioteca, quis aproveitá-la para criar um validador antes de usar o protobuff.

Aproveitando a estrutura da lib ast criei o protobuff aproveitando como ast cria um corpo para seus dados:
```
syntax="proto2";

package expressoes;

message body {
    
    required string _type = 1;
    optional body body = 2;
    optional int32 col_offset = 3;
    optional int32 lineno = 4;
    optional int32 n =5;
    optional body op =6;
    optional body left = 7;
    optional body right = 8;
}
```
Ao criar a equação através de uma string por exemplo “10+10*2”. O ast cria a seguinte estrutura json ao serializá-lo:
```
{'_type': 'Expression', 'body': {'_type': 'BinOp', 'col_offset': 0, 
'left': {'_type': 'Num', 'col_offset': 0, 'lineno': 1, 'n': 10}, 'lineno': 1, 
'op': {'_type': 'Add'}, 
'right': {'_type': 'BinOp', 'col_offset': 3, 
'left': {'_type': 'Num', 'col_offset': 3, 'lineno': 1, 'n': 10}, 'lineno': 1, 
'op': {'_type': 'Mult'}, 'right': {'_type': 'Num', 'col_offset': 6, 'lineno': 1, 'n': 2}}}}

```

Essa estrutura é a mesma do protobuff. Logo pode ser usada a função google.protobuf.json_format.Parse(JSON, OBJ_PROTOBUFF).

Desta forma em seguida  OBJ_PROTOBUFF  pode ser serializado com SerializeToString(). Que retornará a mensagem em formato string e poderá ser enviado no socket python:
```Cliente:
    expre_str_m = “10+10*2” #expressao
    ast_parse_x = ast.parse(expre_str_m, "", "eval") #objeto ast em arvore que valida as exressoes
    ast_json = ast2json(parse(ast_parse_x)) #criando o json a partir de ast
    ast_json_dump_y = json.dumps(ast_json, indent=1) #criando um dump a partir do json, porque eh string e nao json.
    exp_buff_e = body() #usando o body doprotobuff
    msg = json_format.Parse(ast_json_dump_y, exp_buff_e) #transfere os dados do ast_json para o protobuff
    s = exp_buff_e.SerializeToString() #recebendo a string de dados em protobuff - serializacao
    client_socket.sendall(s) #envia por socket o objeto serializado
```

No servidor, a mensagem será recebida pelo socket, um objeto OBJ_PROTOBUFF  será criado e o método ParseFromString(msg) será usado para copiar os dados para o objeto protobuff. Em seguida ele pode fornecer um parser para o tipo dicionário do python. A partir daí a uma função foi criada para recriar a fórmula usada. Não foi possível tornar o JSON no formato ast para o objeto ast. A vantagem de usá-lo foi criar a árvore binária para uma expressão válida. 
```
Servidor:
    print ("Listening")
    message = server_socket.recv(512) #Espera a mensagem chegar
    print("mensagem", message) 
    exp_buff_e = body() #Objeto protobuff
    exp_buff_e.ParseFromString(message) #Copia os dados para o objeto - deserializacao
    mydict = json_format.MessageToDict(exp_buff_e) #Faz o parser para o tipo dicionario do python
    math_e = transform_expression(mydict) #Funcao criada para converter o objeto na expressao
    print("Calcula:", math_e,  eval(math_e)) #Calcula a expressao
    cout = cout+1
    print(cout)
```

2. RMI

Utilizei Pyro4 que é o RMI em python.

Criei a classe Expression que recebe um objeto ast, em set_expression e nela o objeto é decodificado, desserializado com pickle, e em seguida a função astor.to_source pega o objeto e retorna para a expressão original:
```
class Expression(object):
        def __init__(self):
            self.expr = None

        def set_expression(self, expr):
            dec = base64.b64decode(expr['data']) #Decodifica pois esta em base64
            deserialize = pickle.loads(dec) #Desserializa
            rec_expr = astor.to_source(deserialize) #Converte para a expressao inicial
            self.expr = rec_expr #seta o parametro na variavel da classe self.expr que fara o calculo na funcao result

        def result(self):
                result = eval(self.expr) #realiza o calculo da expressao
                print("Expr:", self.expr, "result:", result)
                return result #retorna o resultado
```


No servidor  é criada a função main que inicia o Pyro indicando o nome da Classe que pode ser invocada seguido da URI que ela será acessada.
```
def main():
    Pyro4.Daemon.serveSimple(
            {
                Expression: "david.Expression" 
            },
            host = "192.168.1.110",
            port = 35554,
            ns = False)
```

No cliente foi criado um for com algumas expressões que são convertidas objeto ast, e a serializadas em pickle, esse objeto serializado é passado como parâmetro na função set_expression, a qual já foi programada pra realizar a decodificação, desserialização e setar a variável da classe self.expr para a função result calcular e retornar o valor da expressão.

```
uri = "PYRO:david.Expression@192.168.1.110:35554"
Exp = Pyro4.Proxy(uri)

list_expr = ["(25+8)+(9*7)/(32/8)**2", "(15-8)*3", "(5+9)*(3**2)", "15+15+15+15*3", "2*2*2*2*2+32", "9*9*9", "(1+2)*(3/4)"]
for n in list_expr:
    str_expr = n #Recebe a axpressao
    expr = ast.parse(str_expr, "", "eval") #Converte a expressao em objeto ast
    serialize = pickle.dumps(expr) #serializa o objeto
    Exp.set_expression(serialize) #chama a funcao set_expression com o objeto serializado
    e = Exp.result() #Calcula e retorna o resultado
    print(n, "=", e) #Imprime
```

3. Socket com objeto serializado com pickle sem o protobuff.
```
Cliente:
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
```
```
Servidor:
import compress_pickle as pickle
import json, socket, astor
address = ('localhost', 6005) #endereco do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #configura o socket
server_socket.bind(address) #repassa a conexao

while(1):
    print ("Listening")
    message = server_socket.recv(512) #aguarda os dados chegarem
    deserialize = pickle.loads(message, compression="gzip") #desserializa os dados que chegam
    math_e = astor.to_source(deserialize).replace('\n', '') #converte o objeto na expressao inicial
    print("Calcula", math_e, "=", eval(math_e)) #exibe o resultado
```

Não foi realizado o recebimento da resposta no cliente pois ficou demonstrado o uso da serialização e desserialização, nas situações descritas anteriormente, mostrando que o protobuff poderia ser usado em outras plataformas.

