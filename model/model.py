import itertools

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []

    def creaGrafo(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)
        #for u in self._grafo.nodes:
        #    for v in self._grafo.nodes:
        #        if u != v:
         #           self._grafo.add_edge(u,v)

        myedges = itertools.combinations(self._teams, 2)
        self._grafo.add_edges_from(myedges)

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)