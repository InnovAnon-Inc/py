#import array
#import random

from numpy import min as nmin
from numpy import max as nmax
from numpy import std
from numpy import mean

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from abc        import ABC
from abc        import abstractmethod

from random     import choice
from random     import seed

class SimpleGA(ABC):
    def __init__(self, geneFile):
        self.geneFile = geneFile
        self.genome   = self.load_genome()
    def load_genome(self):
        with open (self.geneFile) as fin: lines = fin.readlines()
        return [line.split() + [""] for line in lines if not line.startswith("#")]
    def generate_individual(self): return list(filter(None, (choice (k) for k in self.genome)))

    @abstractmethod
    def evalOneMax(self, individual): pass

    def setupGA(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        # TODO add genome as primitives

        # Structure initializers
        toolbox.register('indices', self.generate_individual)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
        #toolbox.register("individual", tools.initIterate, creator.Individual, gen_idx)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        #toolbox.register("evaluate", self.evalOneMax)
        toolbox.register("evaluate", lambda individual: self.evalOneMax(individual))
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutNodeReplacement, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        self.toolbox = toolbox

    def runGA(self):
        toolbox = self.toolbox

        seed(64)
    
        pop = toolbox.population(n=300)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", mean)
        stats.register("std", std)
        stats.register("min", nmin)
        stats.register("max", nmax)
        
        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, 
                                       stats=stats, halloffame=hof, verbose=True)
        
        return pop, log, hof

