import json
import sys
import os.path

def automatonType(data):
    '''
        Esta funcao classifica o automato entre os seguintes tipos:
        1: AFD
        2: AFN
        3: AFN&
    '''

    mapEstados = {}
    
    for t in data['transicoes']:
        if t[1] == '&':
            return 3
    
    for t in data['transicoes']:
        if t[0] in mapEstados:
            if t[1] in mapEstados[t[0]]:
                return 2
            else:
                mapEstados[t[0]].append(t[1])
        else:
            mapEstados[t[0]] = [t[1]]
    
    return 1


def main(args):
    assert os.path.exists(args), "Arquivo especificado nao existe."

    with open(args) as arquivo:
        dados = json.load(arquivo)
        
    print(automatonType(dados))
    


if __name__ ==  "__main__":
    assert len(sys.argv) != 1, "Arquivo de entrada nao especificado."
    main(sys.argv[1])
