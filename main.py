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
    afd['estados_finais'] = []
    states = []
    states.append(afn['estado_inicial'])
    processed = []

    while len(states) != 0:
        state = states.pop()

        if state in processed:
            continue
        processed.append(state)

        statelist = state.split('-')

        for e in statelist:
            if e in afn['estados_finais']:
                afd['estados_finais'].append(state)
                continue

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

                states.append(newStateName)
                afd['transicoes'].append([state,c,newStateName])
    afd['estados'] = processed
    return afd


def main(args):
    assert os.path.exists(args), "Arquivo especificado nao existe."

    with open(args) as arquivo:
        automaton = json.load(arquivo)
        
    showAutomaton(automaton)

    if(automatonType(automaton) == 2):
        automaton = conversionAFNtoAFD(automaton)
        showAutomaton(automaton)

    for w in automaton['palavras']:
        print(w + str(": accepted" if accept(automaton,w) else ": rejected"))
    


if __name__ ==  "__main__":
    assert len(sys.argv) != 1, "Arquivo de entrada nao especificado."
    main(sys.argv[1])