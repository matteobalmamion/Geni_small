import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph()
        self._nodes=DAO.getLocalization()
        self._edges=DAO.getConnessioni()
        self._solBest=[]
        self._costBest=0


    def createGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._nodes)
        edges={}
        for edge in self._edges:
            if (edge[0],edge[1]) in edges:
                edges[(edge[0],edge[1])].append(edge[2])
                continue
            elif (edge[1],edge[0]) in edges:
                if edge[2] not in edges[(edge[1],edge[0])]:
                    edges[(edge[1],edge[0])].append(edge[2])
                    continue
            else:
                edges[(edge[0], edge[1])]=[edge[2]]
        for edge in edges:
            value=len(edges[edge])
            self._grafo.add_edge(edge[0],edge[1], weight=value)
    def descriviGrafo(self):
        return self._grafo.nodes, self._grafo.edges
    def getConnected(self,node):
        neighbors=self._grafo.neighbors(node)
        edges=[]
        for neighbor in neighbors:
            edges.append((neighbor,self._grafo[neighbor][node]["weight"]))
        return edges

    def search_path(self,v0):
        self._solBest=[]
        self._costBest=0
        parziale=[]
        visitati=[v0]
        neighbors=self._grafo.neighbors(v0)
        for neighbor in neighbors:
            visitati.append(neighbor)
            parziale.append((v0,neighbor,self._grafo[neighbor][v0]["weight"]))
            self._ricorsione(visitati,parziale,neighbor)
            visitati.pop()
            parziale.pop()
        return self._solBest,self._costBest

    def _ricorsione(self,visitati,parziale,node):
        neighbors=self._admissibleNeighbors(node,visitati)
        if len(neighbors)==0:
            costo=self._calcolaCosto(parziale)
            if costo>self._costBest:
                self._costBest=costo
                self._solBest=copy.deepcopy(parziale)
            print(parziale)
            return
        for neighbor in neighbors:
            visitati.append(neighbor)
            parziale.append((node,neighbor,self._grafo[neighbor][node]["weight"]))
            self._ricorsione(visitati,parziale,neighbor)
            visitati.pop()
            parziale.pop()
    def _admissibleNeighbors(self,node,parziale):
        neighbors=self._grafo.neighbors(node)
        admissible=[]
        for neighbor in neighbors:
            if neighbor not in parziale :
                admissible.append(neighbor)
        return admissible
    def _calcolaCosto(self,parziale):
        sum=0
        for edge in parziale:
            sum+=edge[2]
        return sum

