#import array
#import random

from os         import devnull
from os         import environ
from os         import listdir
from os         import mkdir
from os         import remove
from os         import sep
from os         import walk
from os.path    import exists
from os.path    import isdir
from os.path    import join
from random     import choice
from shutil     import copyfileobj
from shutil     import copytree
from shutil     import rmtree
from subprocess import CalledProcessError
from subprocess import DEVNULL
from subprocess import PIPE
from subprocess import Popen
from subprocess import check_call
from sys        import stdout
from tempfile   import mkdtemp
from timeit     import timeit
from threading  import Thread

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

import numpy

import random
import operator
import csv
import itertools

import numpy

from random import randint, getrandbits
from functools import reduce
from math import log

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from random import randint



class Fuck:
    def __init__(self, fuck):
        self.fuck = fuck

pset = gp.PrimitiveSetTyped("MAIN", (), Fuck)

pset.addPrimitive(Fuck, (int,), Fuck)
pset.addPrimitive(lambda x: x, (int,), int, name="id")

pset.addEphemeralConstant("rand10", lambda: choice([None, 0, 1, 2]), int)






creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def fitness_function(individual):
    # Transform the tree expression in a callable function
    print("individual=%s" % individual)
    stdout.flush()
    cf = toolbox.compile(expr=individual)
    print(cf)
    stdout.flush()
    # TODO
    return randint(-10, 10),
    
toolbox.register("evaluate", fitness_function)

toolbox.register("select", tools.selTournament, tournsize=3)

#toolbox.register("mate", gp.cxOnePoint)
#toolbox.register("mate", gp.cxOnePointLeafBiased, termpb=.7)
toolbox.register("mate", gp.cxOnePointLeafBiased, termpb=.3)
#toolbox.register("mate", gp.cxSemantic, pset=pset)

#toolbox.register("expr_mut", gp.genFull, min_=3, max_=9)
#toolbox.register("expr_mut", gp.genGrow, min_=3, max_=9)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=3, max_=9)

#toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
#toolbox.register("mutate", gp.mutNodeReplacement, pset=pset)
toolbox.register("mutate", gp.mutEphemeral, mode="one")
#toolbox.register("mutate", gp.mutEphemeral, mode="all")
#toolbox.register("mutate", gp.mutInsert, pset=pset)
#toolbox.register("mutate", gp.mutSemantic, pset=pset)

#MAX_HEIGHT = 17
MAX_HEIGHT = 90
toolbox.decorate("mate", gp.staticLimit(operator.attrgetter('height'), MAX_HEIGHT))
toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter('height'), MAX_HEIGHT))












def main():
    print("optimize compiler flags")
    #random.seed(10)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 30, stats, halloffame=hof)

    l = toolbox.compile(expr=hof[0])
    #print("%s => %s => %s" % (hof[0], str(l), reduce(operator.mul, l)))
    #print("%s => %s => %s" % (hof[0], str(l), getS(l)))
    # TODO

    return pop, stats, hof
if __name__ == "__main__": main()
