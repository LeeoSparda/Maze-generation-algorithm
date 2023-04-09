##pip install pyamaze
##pip install pygame

import random

from pyamaze import maze, agent, textLabel, COLOR

# Define a função de busca em profundidade (DFS)
def DFS(m, inicio=None):
    
    # Define a posição inicial
    if inicio is None:
        inicio = (m.rows, m.cols)
    
    # Define as listas de nós explorados e a fronteira de busca
    explorados = [inicio]
    fronteira = [inicio]
    
    # Cria um dicionário para armazenar o caminho percorrido durante a busca
    armezenaCaminhoPercorrido = {}
    
    # Cria uma lista para armazenar a ordem em que os nós foram explorados
    guardarNos = []
    
    # Executa a busca em profundidade
    while len(fronteira) > 0:
        
        # Retira um nó da fronteira
        no = fronteira.pop()

        
        # Adiciona o nó à lista de busca
        guardarNos.append(no)
        
        # Verifica se o nó atual é o objetivo
        if no == m._goal:
            break
        
        # Inicializa um contador para verificar quantos filhos o nó atual tem
        cont = 0
        
        # Percorre os vizinhos do nó atual
        for d in 'ESNW':
            
            # Verifica se o vizinho é alcançável
            if m.maze_map[no][d] == True:
                
                # Define a posição do vizinho
                if d == 'E':
                    vizinho = (no[0], no[1]+1)
                if d == 'W':
                    vizinho = (no[0], no[1]-1)
                if d == 'N':
                    vizinho = (no[0]-1, no[1])
                if d == 'S':
                    vizinho = (no[0]+1, no[1])
                
                # Verifica se o vizinho já foi explorado
                if vizinho in explorados:
                    continue
                
                # Incrementa o contador de filhos
                cont += 1
                
                # Adiciona o vizinho à lista de nós explorados e à fronteira de busca
                explorados.append(vizinho)
                fronteira.append(vizinho)
                
                # Armazena o caminho percorrido
                armezenaCaminhoPercorrido[vizinho] = no
        
        # Verifica se o nó atual é um ponto de bifurcação
        if cont > 1:
            m.markCells.append(no)
    
    # Cria um dicionário para armazenar o caminho percorrido do objetivo até o início
    guardaCaminho = {}
    
    # Define a posição do nó atual como sendo o objetivo
    posAtual = m._goal
    
    # Percorre o caminho percorrido pela busca em profundidade, do objetivo até o início
    while posAtual != inicio:
        guardaCaminho[armezenaCaminhoPercorrido[posAtual]] = posAtual
        posAtual = armezenaCaminhoPercorrido[posAtual]
    
    # Retorna a lista de busca, o caminho percorrido e o caminho percorrido do objetivo até o início
    return guardarNos, armezenaCaminhoPercorrido, guardaCaminho

if __name__=='__main__':

    LARGURA_LABIRINTO = int(input("Digite a largura do labirinto: "))
    ALTURA_LABIRINTO = int(input("Digite a altura do labirinto: "))

    # Cria um labirinto de 20x20 e gera um novo labirinto aleatório com o ponto de partida em (2,4)
    m=maze(LARGURA_LABIRINTO,ALTURA_LABIRINTO) 
    m.CreateMaze(2,4) 

    # Executa a busca em profundidade a partir do ponto de partida (5,1)
    guardarNos,armezenaCaminhoPercorrido,guardaCaminho=DFS(m,(5,1)) 

    # Cria três agentes: 
    # a é o agente verde que começa no ponto de partida (5,1) e tem como objetivo chegar em (2,4)
    # b é o agente que começa no objetivo (2,4) e segue o caminho encontrado pela busca em profundidade
    # c é o agente amarelo que segue o caminho encontrado pela busca em largura
    a=agent(m,5,1,goal=(2,4),footprints=True,shape='square',color=COLOR.green)
    b=agent(m,2,4,goal=(5,1),footprints=True,filled=True)
    c=agent(m,5,1,footprints=True,color=COLOR.yellow)

    # Traça o caminho percorrido pela busca em profundidade do agente a (marcado) e o caminho encontrado pelos agentes b e c
    m.tracePath({a:guardarNos},showMarked=True)
    m.tracePath({b:armezenaCaminhoPercorrido})
    m.tracePath({c:guardaCaminho})

    # Executa o labirinto
    m.run()

    # Cria um novo labirinto a partir de um arquivo CSV (que contém as informações do labirinto)
    m=maze()
    # m.CreateMaze(loadMaze='dfs.csv')

    # Executa a busca em profundidade no novo labirinto
    guardarNos,armezenaCaminhoPercorrido,guardaCaminho=DFS(m)

    # Cria três agentes:
    # a é o agente verde que começa em uma posição aleatória no novo labirinto
    # b é o agente que começa no ponto (1,1) e tem como objetivo chegar em (5,5)
    # c é o agente amarelo que segue o caminho encontrado pela busca em largura
    a=agent(m,footprints=True,shape='square',color=COLOR.green)
    b=agent(m,1,1,goal=(5,5),footprints=True,filled=True,color=COLOR.cyan)
    c=agent(m,footprints=True,color=COLOR.yellow)

    # Traça o caminho percorrido pela busca em profundidade do agente a (marcado) e o caminho encontrado pelos agentes b e c
    m.tracePath({a:guardarNos},showMarked=True)
    m.tracePath({b:armezenaCaminhoPercorrido})
    m.tracePath({c:guardaCaminho})

    # Executa o labirinto
    m.run()