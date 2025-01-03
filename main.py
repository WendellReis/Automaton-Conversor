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

def AFNtoAFD(afn):
    '''
        Essa funcao converter um dado AFN em um AFD equivalente
    '''

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

        statelist = state.split(',')

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
                    newStateName = newStateName + ',' + newState[i]

                states.append(newStateName)
                afd['transicoes'].append([state,c,newStateName])
    afd['estados'] = processed
    return afd

def advanceState(s,c,t):
    states = []
    for i in t:
        if s == i[0] and c == i[1]:
            states.append(i[2])
    return sorted(set(states))

def AFNEtoAFN(afne):
    '''
        Essa funcao converte um dado AFNE em um AFN equivalente
    '''

    afn = afne.copy()
    afn['transicoes'] = []

    closures = {}
    for s in afne['estados']:
        closures[s] = epsilonClosure(s,afne['transicoes'])
    
    for s in afne['estados']:
        for c in afne['alfabeto']:
            states = []
            for i in closures[s]:
                for j in advanceState(i,c,afne['transicoes']):
                    states = states + closures[j]

            for i in sorted(set(states)):
                afn['transicoes'].append([s,c,i])
        
    return afn

def epsilonClosure(s,t):
    '''
        Funcao que retorna o fecho epsulon de um dado estado s em um conjunto t de transicoes
    '''
    if s == '&':
        return []
    
    closure = [s]

    for i in t:
        if i[0] == s and i[1] == '&':
            for j in epsilonClosure(i[2],t):
                closure.append(j)
    
    return sorted(set(closure))

def markTable(i,j,mat):
    if mat[i][j] == [0]:
        return

    cels = mat[i][j]
    mat[i][j] = [0]

    for k in cels:
        markTable(k[0],k[1],mat)

def uniteStates(s1,s2,afd):
    newState = str(s1) + "," + str(s2)

    if afd['estado_inicial'] in [s1,s2]:
        afd['estado_inicial'] = newState

    afd['estados'] = [s if s != s1 and s != s2 else newState for s in afd['estados']]

    if newState in afd['estados_finais']:
        afd['estados_finais'].append(newState)

    while True:
        for i in afd['estados_finais']:
            if i in [s1,s2]:
                afd['estados_finais'].remove(i)
                continue
        break

    for i in range(len(afd['transicoes'])):
        if afd['transicoes'][i][0] in [s1,s2]:
            afd['transicoes'][i][0] = newState
        if afd['transicoes'][i][2] in [s1,s2]:
            afd['transicoes'][i][2] = newState

def minimizeAFD(afd):
    # Adicionando estado coringa
    jokerState = False

    for s in afd['estados']:
        for c in afd['alfabeto']:
            find = False
            for t in afd['transicoes']:
                if t[0] == s and t[1] == c:
                    find = True
                    break
            if not find:
                jokerState = True
                afd['transicoes'].append([s,c,","])
    
    if jokerState:
        afd['estados'].append(",")
        for c in afd['alfabeto']:
            afd['transicoes'].append([",",c,","])

    tam = len(afd['estados'])


    mat = [[[] for _ in range(tam)] for _ in range(tam)]

    # Marcar estados trivialmente nao equivalentes
    for i in range(tam):
             for j in range(i+1,tam):
                if ((i in afd['estados_finais']) ^ (j in afd['estados_finais'])) or afd['estados'][i] == "," or afd['estados'][j] == ",":
                    mat[i][j] = [0]

    id = {}
    for i in range(tam):
        id[afd['estados'][i]] = i

    for i in range(tam):
             for j in range(i+1,tam):
                 if mat[i][j] == [0]:
                     continue
                 
                 for c in afd['alfabeto']:
                    pi = id[advanceState(afd['estados'][i],c,afd['transicoes'])[0]]
                    pj = id[advanceState(afd['estados'][j],c,afd['transicoes'])[0]]

                    if pi == pj:
                        continue
                
                    if pj < pi:
                        temp = pj
                        pj = pi
                        pi = temp
                    
                    if mat[pi][pj] != [0]:
                        mat[pi][pj].append([i,j])
                    else:
                        markTable(i,j,mat)

    # Unindo estados nao marcados na matriz
    while True:
        for i in range(tam):
            for j in range(i+1,tam):
                if mat[i][j] != [0]:
                    uniteStates(i,j,afd)
                    mat[i][j] = [0]
                    continue

        break


    # Removendo estado coringa
    if jokerState:
        afd['estados'].remove(",")
        transicions = []
        for t in afd['transicoes']:
            if t[0] != "," and t[2] != ",":
                transicions.append(t)
                    
        afd['transicoes'] = transicions
    return afd
                    
def main(args):
    assert os.path.exists(args), "Arquivo especificado nao existe."

    with open(args) as arquivo:
        automaton = json.load(arquivo)
    
    print('Automato Recebido:')
    showAutomaton(automaton)

    if automatonType(automaton) == 3:
        print('\nConversao AFN& -> AFN Minimizado:')
        automaton = AFNEtoAFN(automaton)
        showAutomaton(automaton)

    if automatonType(automaton) == 2:
        print('\nConversao AFN -> AFD Minimizado:')
        automaton = AFNtoAFD(automaton)
        showAutomaton(automaton)

    automaton = minimizeAFD(automaton)
    print('\nAFD Minimizado:')
    showAutomaton(automaton)

    if len(automaton['palavras']):
        print('\nResultados do reconhecimendo das palavras:')
        for w in automaton['palavras']:
            print(w + str(": aceita" if accept(automaton,w) else ": rejeitada"))
    
if __name__ ==  "__main__":
    assert len(sys.argv) != 1, "Arquivo de entrada nao especificado."
    main(sys.argv[1])
