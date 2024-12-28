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

def showAutomaton(data):
    tipo = ['AFD','AFN','AFN&']
    print("Tipo: " + tipo[automatonType(data)-1])
    print("Alfabeto: ",end='')
    print(data['alfabeto'])
    print("Estados: " + str(data['estados']))
    print("Estado Inicial: " + str(data['estado_inicial']))
    print("Estados Finais: " + str(data['estados_finais']))
    print("Transicoes: [")
    for t in data['transicoes']:
        print('\t'+str(t))
    print("]")

def accept(automaton,word):
    state = automaton['estado_inicial']

    if word == "&":
        return state in automaton['estados_finais']

    for c in word:
        find = False
        for t in automaton['transicoes']:
            if t[0] == state and t[1] == c:
                state = t[2]
                find = True
                break
        if not find:
            return False
    return state in automaton['estados_finais']

def main(args):
    assert os.path.exists(args), "Arquivo especificado nao existe."

    with open(args) as arquivo:
        data = json.load(arquivo)
        
    showAutomaton(data)

    for w in data['palavras']:
        print(w + str(": accepted" if accept(data,w) else ": rejected"))
    


if __name__ ==  "__main__":
    assert len(sys.argv) != 1, "Arquivo de entrada nao especificado."
    main(sys.argv[1])