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
    '''
        Essa funcao exibe as informacoes de um automato
    '''
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

def accept(afd,word):
    '''
        Funcao que verifica se um dado automato reconhece uma palavra
    '''
    state = afd['estado_inicial']

    if word == "&":
        return state in afd['estados_finais']

    for c in word:
        find = False
        for t in afd['transicoes']:
            if t[0] == state and t[1] == c:
                state = t[2]
                find = True
                break
        if not find:
            return False
    return state in afd['estados_finais']

def conversionAFNtoAFD(afn):
    afd = afn.copy()
    afd['transicoes'] = []
    states = [afn['estado_inicial']]
    processed = []

    while len(states) != 0:
        state = states.pop()
        statelist = state.split('-')

        for c in afn['alfabeto']:
            newState = []
            for t in afn['transicoes']:
                if t[0] in statelist and t[1] == c and t[2] not in newState:
                    newState.append(t[2])
            
            if len(newState) > 0:
                newState.sort()
                newStateName = newState[0]

                for i in range(1,len(newState)):
                    newStateName = newStateName + '-' + newState[i]

                if newStateName not in processed:
                    states.append(newStateName)
                    afd['transicoes'].append([state,c,newStateName])
                    processed.append(state)
    return afd


def main(args):
    assert os.path.exists(args), "Arquivo especificado nao existe."

    with open(args) as arquivo:
        data = json.load(arquivo)
        
    showAutomaton(data)

    if(automatonType(data) == 2):
        showAutomaton(conversionAFNtoAFD(data))

    for w in data['palavras']:
        print(w + str(": accepted" if accept(data,w) else ": rejected"))
    


if __name__ ==  "__main__":
    assert len(sys.argv) != 1, "Arquivo de entrada nao especificado."
    main(sys.argv[1])