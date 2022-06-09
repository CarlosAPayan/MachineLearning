# -*- coding: utf-8 -*-
"""
@Module: Metaheurísticas
@Author: Payán Rosales Carlos A.
@Topic: Búsqueda Tabú
"""
import random, math
import numpy as np
import pandas as pd

class FlowShop:
    def __init__(self,jobs):
        self.d_jobs=jobs
        self.d_process = len(jobs[0])
        self.n_jobs=len(self.d_jobs)
        self.size=math.factorial(self.n_jobs)

    def solucionVecina(self,current_sol):
        x1 = np.random.randint(0,self.n_jobs)
        while True:
            x2 = np.random.randint(0,self.n_jobs)
            if x1 != x2:
                break
        new=current_sol.copy()
        new[x1],new[x2] = current_sol[x2],current_sol[x1]
        return new, x1, x2

    def solucionInicial(self):
        index=list(range(self.n_jobs))
        random.shuffle(index)
        #return tuple(index)
        return index

    def makespan(self,state):
        temp=[]
        for i in state:
            temp.append(np.array(self.d_jobs[i]))
        cost=np.array(temp)
        for i in range(self.d_process):
            for j in range(self.n_jobs):
                temp=cost[0:j+1,0:i+1].copy()
                temp[-1][-1]=0
                cost[j][i]+=np.max(temp)
        return cost[-1][-1]

class TabuSearch:
    def __init__(self,problem):
        self.problem = problem
        self.f = self.problem.makespan
        self.sI = problem.solucionInicial()
        self.vecSize = 30

    def neighborhood(self):
        neighbors = []
        movements = []
        for i in range(self.vecSize):
            sV,x1,x2 = self.problem.solucionVecina(self.sI) #Se genera un vecino
            move = str(x1) + "," + str(x2)
            neighbors.append(sV)
            movements.append(move)

        return neighbors,movements

    def start(self):
        tabuList = {}
        lstm = {} #long-short term memory / memoria a largo plazo
        self.best = self.sI
        diff,it = 0,0
        difLocal = 0
        mejorLocal = self.sI
        band = True
        while it <= 100:
            it += 1
            #Se crea el vecindario
            neighbors, movements = self.neighborhood()
            if it%1000==0:
                band = not band
            if band:
                liberar = []
                for clave in tabuList: #Se despenaliza cada elemento en cada iteración
                    tabuList[clave] -= 1
                    if tabuList[clave] == 0:
                        liberar.append(clave)

                #Se liberan los elementos de la TabuList con penalización 0
                for item in liberar:
                    free = tabuList.pop(item)

                for _ in range(self.vecSize):
                    sV = neighbors[_]
                    move = movements[_]
                    ΔE = self.f(sV) - self.f(self.sI) #Se compara si la solución vecina mejora el resultado
                    if ΔE <= 0:
                        #Se acepta la solución pero se Comprueba si la solución no está en la TabuList
                        if difLocal > ΔE:
                            if move in tabuList.keys():
                                #Criterio de aspiración
                                if ΔE < diff:
                                    self.best = self.sI = sV
                                    diff = ΔE
                                    iteraBest = it
                                    tabuList[move] = 3 #ingresa el movimiento a la TabuList
                                    if move in lstm.keys(): #Se agrega el registro a LongShortTermMemory
                                        lstm[move] += 1
                                    else:
                                        lstm[move] = 1
                            else:
                                mejorLocal = self.sI = sV #Acepta la solución y actualiza los datos iniciales
                                difLocal = ΔE
                                itera = it
                                tabuList[move] = 3 #ingresa el movimiento a la TabuList
                                if move in lstm.keys():#Se agrega el registro a LongShortTermMemory
                                    lstm[move] += 1
                                else:
                                    lstm[move] = 1

                    if difLocal < diff:
                        self.best = mejorLocal
                        diff = difLocal
                        iteraBest = itera
            else: #LSTM
                maX = 0
                rep = None
                for item in lstm:
                    if lstm[item] > maX:
                        maX = lstm[item]
                        rep = item

                for _ in range(self.vecSize):
                    sV = neighbors[_]
                    move = movements[_]
                    ΔE = self.f(sV) - self.f(self.sI) #Se compara si la solución vecina mejora el resultado
                    if ΔE <= 0:
                        #Se acepta la solución pero se Comprueba si la solución no está en la TabuList
                        if difLocal > ΔE:
                            if lstm[move] > maX/2:
                                pass
                            else:
                                difLocal = ΔE
                                mejorLocal = move
                                itera = it
                                if move in lstm.keys():#Se agrega el registro a LongShortTermMemory
                                    lstm[move] += 1
                                else:
                                    lstm[move] = 1

                    if difLocal < diff:
                        self.best = mejorLocal
                        diff = difLocal
                        iteraBest = itera

        return self.best, lstm, iteraBest

if __name__ == '__main__':
    #data = pd.read_csv('Instancia1.csv',header=None)
    #data = pd.read_csv('Instancia2.csv',header=None)
    data = pd.read_csv('Instancia3.csv',header=None)
    inst = data.values.tolist()
    flowShopScheduling = FlowShop(inst)
    model = TabuSearch(flowShopScheduling)
    result,lstm, itera = model.start()
    cost = flowShopScheduling.makespan(result)
    print("\n  | Búsqueda Tabú | \n")
    print(f" Solución: {result}\n Costo: {cost}\n Iteración: {itera}")
