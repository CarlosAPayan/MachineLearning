#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 17:50:36 2022

@author: Payán Rosales Carlos A.
"""

from cmath import inf
from random import shuffle
import numpy as np
import pandas as pd

class FSS:
    def __init__(self, jobs):
        self.d_jobs=jobs
        self.n_jobs=len(self.d_jobs[0])
        self.n = len(self.d_jobs)
    def sol_inicial(self):
        y = list(range(self.n))
        shuffle(y)
        return y

    def costo(self,state):
        temp=[]
        for i in state:
            temp.append(np.array(self.d_jobs[i]))
        cost=np.array(temp)
        for i in range(self.n_jobs):
            for j in range(len(self.d_jobs)):
                temp=cost[0:j+1,0:i+1].copy()       #Se crea una copia del vector del trabajo 
                temp[-1][-1]=0                      #Donde en la ultima posición se guarda 
                cost[j][i]+=np.max(temp)            #El tiempo de procesamiento total de las tareas
        return cost[-1][-1]
        

        
class GeneticAlgorithm:
    def __init__(self, problem):
        self.p = problem
        self.f = self.p.costo
        self.pobSize = 100
        self.nSols = []
        self.generations = 100
        
    def poblacion_inicial(self):
        pob = []
        y = self.p.sol_inicial()
        pob.append(y)
        x = 1
        while x < min(self.pobSize,5000):
            y = self.p.sol_inicial()
            if y not in pob:
                pob.append(y)
                x+=1
        #print("Pass first population")        
        return pob
    
    def selection(self, pob):
        #Selección de los individuos a cruzar
        padres = []
        #padres = self.torneo(pob)
        padres = self.ruleta(pob)
        #print("Selection ended")        
        return padres
    
    def crossover(self, padres):
        siGen = []

        for i in range(1,len(padres)):
            newIndiv = self.cruza(padres[i-1], padres[i])
            newIndiv = self.mutation(newIndiv)
            siGen.append(newIndiv)
        #print("Pass crossover")    
        return siGen
        
    def cruza(self, a,b):
        p1,p2 = np.random.randint(self.p.n), np.random.randint(self.p.n)
        p1,p2 = min(p1,p2), max(p1,p2)
        prod = np.zeros_like(a)-1
        for i, x in enumerate(a):
            if i > p1 and i < p2:
                prod[i] = x
        for i, x in enumerate(b):
            if i < p1 or i > p2:
                if x not in prod:
                    prod[i] = x
        for i,x in enumerate(prod):
            if x == -1:
                for id in b:
                    if id not in prod:
                        prod[i] = id
        return prod
        
        
    def mutation(self, indiv, rateMutation = 0.01):
        newIndiv = indiv.copy()
        mutate = np.random.random()
        if mutate <= rateMutation:
            while True:
                x1,x2 = np.random.randint(self.p.n),np.random.randint(self.p.n)
                if x1 != x2:
                    break
                
            newIndiv[x1],newIndiv[x2] = indiv[x2],indiv[x1]
        #print("Pass mutation")    
        return newIndiv
    
    def fit(self):
        bestScore = inf
        maxSols = []
        pob = self.poblacion_inicial()
        gen = 0
        for epoch in range(1, self.generations+1):
            for ind in pob:
                new = self.f(ind)
                if new < bestScore:
                    maxSols = list(ind).copy()
                    bestScore = new
                    gen = epoch
                    #print(bestScore)
            
            pad = self.selection(pob)
            pob = self.crossover(pad)
            pob.append(maxSols)
            print(f"Generación: {gen} \n Costo minimo: {self.f(maxSols)} \n\t Mejor solución: {maxSols}")
            
        
    def torneo(self, pob):
        padres = []
        #Torneo
        mejor = None
        while True:
            #print(f"{len(padres)} padres")
            if len(padres) == 10:
                #padres = padres + pob[:8]
                break
            else:
                minimo = self.p.n
                p = [np.random.randint(self.p.n) for i in range(self.p.n//2)]
                #print(p)
                #x = input()
                for i in p:
                    cost = self.f(pob[i])
                    if cost < minimo:
                        minimo = cost
                        mejor = pob[i]
                    
                if mejor not in padres:
                    padres.append(mejor)
        return padres
    
    def ruleta(self, pob):
        padres = []
        arr = np.array([self.f(p)+1 for p in pob])
        arr = 1/np.array(arr)
        arr = arr/sum(arr)
        for i,x in enumerate(arr):
            if i > 0:
                arr[i] = x+arr[i-1]
        
        for _ in range(self.pobSize):
            rd = np.random.random()
            for i,x in enumerate(arr):
                m = 0
                if rd >= m and rd <= x:
                    padres.append(pob[i])
                    break
        return padres
    
if __name__ == '__main__':
    problem = pd.read_csv('Instancia4.csv')
    data = problem.to_numpy()
    nQ = FSS(data)
    aG = GeneticAlgorithm(nQ)
    aG.fit()
