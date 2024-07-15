import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.DiGraph()
        self._grafo2=nx.DiGraph()
        self._solBest=[]
        self._costBest=0

    def create_graph(self):
        self._grafo.clear()
        self._nodes=DAO.getChromosone()
        for node in self._nodes:
            self._grafo.add_node(node)
        self._edges=DAO.getEdges()
        for edge in self._edges:
            if self._grafo.has_edge(edge.Chromosome1,edge.Chromosome2) :
                    self._grafo[edge.Chromosome1][edge.Chromosome2]["corr"]+=edge.corr
            else:
                self._grafo.add_edge(edge.Chromosome1,edge.Chromosome2, corr=edge.corr)

    def getNumberOfNodes(self):
        return self._grafo.number_of_nodes()

    def getNumberOfEdges(self):
        return self._grafo.number_of_edges()
    def getMinEdge(self):
        min=(0,0,20)
        for edge in self._grafo.edges:
            if self._grafo.edges[edge]["corr"]<min[2]:
                min=(edge[0],edge[1],self._grafo.edges[edge]["corr"])
            print(edge)
        return min

    def getMaxEdge(self):
        min = (0, 0, -20)
        for edge in self._grafo.edges:
            if self._grafo.edges[edge]["corr"]>min[2]:
                min=(edge[0],edge[1],self._grafo.edges[edge]["corr"])
            print(edge)
        return min

    def countEdges(self,nMin):
        min=0
        max=0
        ugu=0
        self._grafo2.add_nodes_from(list(self._grafo.nodes))
        for edge in self._grafo.edges:
            if self._grafo.edges[edge]["corr"]>nMin:
                max+=1
                self._grafo2.add_edge(edge[0],edge[1],corr=self._grafo.edges[edge]["corr"])
            elif self._grafo.edges[edge]["corr"]<nMin:
                min+=1
            else:
                ugu+=1
        return min,max,ugu
    def search_path(self,t):
            for n in self.get_nodes():
                partial = []
                partial_edges = []

                partial.append(n)
                self.ricorsione(partial, partial_edges, t)

            print("final", len(self._solBest), [i[2]["corr"] for i in self._solBest])

    def ricorsione(self, partial, partial_edges, t):
            n_last = partial[-1]
            neigh = self.getAdmissibleNeighbs(n_last, partial_edges, t)

            # stop
            if len(neigh) == 0:
                weight_path = self.computeWeightPath(partial_edges)
                weight_path_best = self.computeWeightPath(self._solBest)
                if weight_path > weight_path_best:
                    self._solBest = partial_edges[:]
                return

            for n in neigh:
                partial.append(n)
                partial_edges.append((n_last, n, self._grafo.get_edge_data(n_last, n)))
                self.ricorsione(partial, partial_edges, t)
                partial.pop()
                partial_edges.pop()

    def getAdmissibleNeighbs(self, n_last, partial_edges, t):
            all_neigh = self._grafo.edges(n_last, data=True)
            result = []
            for e in all_neigh:
                if e[2]["corr"] > t:
                    e_inv = (e[1], e[0], e[2])
                    if (e_inv not in partial_edges) and (e not in partial_edges):
                        result.append(e[1])
            return result

    def computeWeightPath(self, mylist):
            weight = 0
            for e in mylist:
                weight += e[2]['corr']
            return weight

    def getSolBest(self):
        return self._solBest
    def getCostoBest(self):
        return self._costBest

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))
