import copy
import itertools
import random

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = {}
        self._bestPath = []
        self._bestObjVal = 0

    def getPath(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        for v in self._grafo.neighbors(v0):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()

    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0])
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObjVal

    def _ricorsione(self, parziale):
        #condizione di ottimalità, verifico se parziale è il migliore
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        #

        # faccio la ricorsione
        for v in self._grafo.neighbors(parziale[-1]):
            pesoE = self._grafo[parziale[-1]][v]["weight"]

            if self._grafo[parziale[-2]][parziale[-1]]["weight"] > pesoE and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def _ricorsioneV2(self, parziale):
        # condizione di ottimalità, verifico se parziale è il migliore
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        #

        # faccio la ricorsione
        listaVicini = self.getVicini(parziale[-1])

        for v in listaVicini:
            if v[0] not in parziale and self._grafo[parziale[-2]][parziale[-1]]["weight"] > v[1]:
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return


    def _score(self, parziale):
        score = 0
        for i in range(0,len(parziale)-1):
            score+=self._grafo[parziale[i]][parziale[i+1]]["weight"]

        return score


    def creaGrafo(self, year):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams)
        #for u in self._grafo.nodes:
        #    for v in self._grafo.nodes:
        #        if u != v:
         #           self._grafo.add_edge(u,v)

        myedges = list(itertools.combinations(self._teams, 2))
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesofTeam(year, self._idMapTeams)
        for e in self._grafo.edges:
            sal1 = mapSalary[e[0]]
            sal2 = mapSalary[e[1]]
            peso = sal1+sal2
            self._grafo[e[0]][e[1]]["weight"] = peso

    def getVicini(self, source):
        vicini = self._grafo.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._grafo[source][v]["weight"]))
        return viciniTuples

    def getAllYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._teams = DAO.getTeamsOfYear(year)
        self._idMapTeams = {t.ID: t for t in self._teams}
        return self._teams

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getRandomNode(self):
        index = random.randint(0,len(self._teams))
        return self._teams[index]
