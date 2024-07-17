import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.DiGraph()
        self._solBest=[]
        self._costBest=0

    def create_graph(self):
        self._grafo.clear()
        nodes=DAO.getChromosomes()
        edges=DAO.getConnections()
        self._grafo.add_nodes_from(nodes)
        self._min=(0,0,1000)
        self._max=(0,0,-1000)
        for edge in edges:
            self._grafo.add_edge(edge[0],edge[1], weight=float(edge[2]))
            if float(edge[2])<self._min[2]:
                self._min=(edge[0],edge[1], float(edge[2]))
            if float(edge[2])>self._max[2]:
                self._max=(edge[0],edge[1], float(edge[2]))
        return self._min,self._max
    def describeGrpah(self):
        return self._grafo.nodes, self._grafo.edges
    def searchEdges(self,soglia):
        minori=[]
        maggiori=[]
        uguali=[]
        for edge in self._grafo.edges:
            weight=self._grafo.get_edge_data(edge[0],edge[1])["weight"]
            if weight<soglia:
                minori.append(edge)
            elif weight>soglia:
                maggiori.append(edge)
            else:
                uguali.append(edge)
        return minori,maggiori,uguali
    def searchPath(self,soglia):
        self._costBest=0
        self._solBest=[]
        parziale=[]
        visitati=[]
        for node in self._grafo.nodes:
            visitati.append(node)
            self._ricorsione(visitati,parziale,soglia)
            visitati.pop()
        return self._solBest,self._costBest

    def _ricorsione(self,visitati,parziale,soglia):
        v0=visitati[-1]
        neighbors=self._admissibleNeighbors(v0,parziale,soglia)
        if len(neighbors)==0:
            if self._costBest<self._sumWeight(parziale):
                self._costBest=self._sumWeight(parziale)
                self._solBest=copy.deepcopy(parziale)
            return
        for neighbor in neighbors:
            visitati.append(neighbor)
            parziale.append((v0,neighbor, self._grafo[v0][neighbor]["weight"]))
            self._ricorsione(visitati,parziale,soglia)
            visitati.pop()
            parziale.pop()
    def _admissibleNeighbors(self,v0,parziale,soglia):
        admissible=[]
        neighbors=self._grafo.neighbors(v0)
        for neighbor in neighbors:
            if self._grafo[v0][neighbor]["weight"]>soglia:
                if (v0,neighbor,self._grafo[v0][neighbor]["weight"]) not in parziale:
                    admissible.append(neighbor)
        return admissible

    def _sumWeight(self,parziale):
        sum=0
        for edge in parziale:
            sum+=edge[2]
        return sum