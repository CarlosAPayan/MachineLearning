#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 22:54:07 2022

@author: Payán Rosales Carlos A.
"""
from cmath import inf
from random import shuffle
import numpy as np
from FlowShop import FSS
import pandas as pd

class ACO:
    def __init__(self, problem):
        self.problem = problem
        self.f = problem.costo
        self.nAnts = 15
        self.nAntsLeavePheromones = 3
        self.iterations = 3
        self.extintPheromoneRate = 0.7
        self.expPheromone = 1.
        self.expMakespan = 1.
        self.pheromones = np.zeros(self.problem.n, dtype=float)
    
    def leavePheromones(self, agregados, dosis):
        for i in range(agregados):
            self.pheromones[agregados[i]] += dosis 
    
    def lostPheromones(self):
        #Se va evaporando cada feromona
        for p in range(len(self.pheromones)):
            self.pheromones[p] *= 0.9
            
    def chooseJob(self, agregados):
        current = agregados[-1]
        avaiables = []
        maks = []
        for i in range(self.problem.n):
            if i not in agregados:
                prop = agregados
                prop.append(i)
                pheromone = np.power(1.+ self.pheromones[i], self.expPheromone)
                makespan = np.power(1./self.f(prop),self.expMakespan) * pheromone
                avaiables.append(i)
                maks.append(makespan)
                
        index = maks.index(min(maks))
        return avaiables[index]
    
    def chooseSchedule(self):
        schedule = [np.random.randint(self.problem.n)]
        
        while len(schedule) < self.problem.n:
            schedule.append(self.chooseJob(schedule))
            
        return schedule[:-1]
                
        
    def run(self):
        bestSol = self.problem.sol_inicial()
        minMakespan = self.f(bestSol)
        g = 0
        for gen in range(self.iterations):
            ants = self.createAnts()
            for anty in ants:
                cost = self.f(anty)
                if cost < minMakespan:
                    g = gen
                    minMakespan = cost
                    bestSol = anty
            
        print(f"Iteración: {g}  Makespan: {minMakespan}\n Bestsol:\n {bestSol}")
        #return bestSol
        
    def createAnts(self):
        ants = []
        for numAnt in range(self.nAnts):
            ants.append(self.chooseSchedule())
        return ants
    
if __name__ == '__main__':
    problem = pd.read_csv('Instancia3.csv')
    data = problem.to_numpy()
    fs = FSS(data)
    Aco = ACO(fs)
    Aco.run()
