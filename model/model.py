import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.year=0
        self.color=None
        self.g=nx.Graph()
        self.idMap={}
        self.source=None
        self.BP=[]
        self.lenMax=0
        pass
    def getColors(self):
        return DAO.getColors()
    def creaGrafo(self, year,color):

        self.g.clear()
        self.vertici=DAO.getProdottiColorati(color)
        for v in self.vertici:
            self.idMap[v.Product_number]=v
        self.g.add_nodes_from(self.vertici)
        print(self.g)
        edges=DAO.getEdges(year,color)
        for edge in edges:
            u=self.idMap[edge[0]]
            v=self.idMap[edge[1]]
            peso=edge[2]
            self.g.add_edge(u,v,weight=peso)
        print(self.g)

    def getPesanti(self):
        listaTuple=[]
        for u,v,data in self.g.edges(data=True):
            listaTuple.append((u.Product_number,v.Product_number,data["weight"]))
        listaTuple.sort(key=lambda x:x[2], reverse=True)
        listaNew=listaTuple[:3]
        ripetuti={}
        for x in listaNew:
            if x[0] not in ripetuti:
               ripetuti[ x[0]]=1
            else:
                ripetuti[x[0]] = 1
            if x[1] not in ripetuti:
                ripetuti[x[1]]=1
            else:
                ripetuti[x[1]]+=1
        y = list(filter(lambda x: ripetuti[x] > 1, ripetuti.keys()))
        return listaNew,y
    def getBP(self, idNode):
        self.source=self.idMap[int(idNode)]
        parziale=[self.source]
        archiVisitati=[]
        listaVis=self.getVisitabili(self.source,archiVisitati,0)
        for v in listaVis:
            parziale.append(v)
            ultimoPeso=self.g[v][self.source]["weight"]
            archiVisitati.append((v,self.source))
            archiVisitati.append((self.source,v))
            self.ricorsione(parziale,archiVisitati,ultimoPeso)
            parziale.pop()
            archiVisitati.pop()
            archiVisitati.pop()


    def ricorsione(self, parziale,archiVisitati,ultimoPeso):
        #check if best
        if len(parziale)-1>self.lenMax:
            self.lenMax=len(parziale)-1
            self.BP=copy.deepcopy(parziale)
            print(self.lenMax)
        listaVis = self.getVisitabili(parziale[-1], archiVisitati, ultimoPeso)
        if len(listaVis)==0:
            return
        for v in listaVis:
            parziale.append(v)
            ultimoPeso=self.g[v][parziale[-2]]["weight"]
            archiVisitati.append((v,parziale[-2]))
            archiVisitati.append((parziale[-2],v))
            self.ricorsione(parziale,archiVisitati,ultimoPeso)
            parziale.pop()
            archiVisitati.pop()
            archiVisitati.pop()





    def getVisitabili(self, source, archiVisitati, ultimoPeso):
        listaV=[]
        for n in self.g.neighbors(source):
            if self.g[n][source]["weight"]>=ultimoPeso and (n,source) not in archiVisitati:

                listaV.append(n)
        return listaV












