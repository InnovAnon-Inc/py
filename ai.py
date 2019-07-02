"""
# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
"""

from keras.initializers import Initializer, Zeros, Ones, Constant

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

class Model:
    def __init__(self, layers, loss, optimizer, last_activation, last_kernel_initializer, last_bias_initializer):
        self.layers     = layers
        self.loss       = loss
        self.optimizer  = optimizer
        self.last_layer = Layer(1, last_activation, last_kernel_initializer, last_bias_initializer)
    def createModel(self):
        self.model = Sequential()
        layers.append(last_layer)
        for layer in layers:
            layer.createLayer()
            self.model.add(layer.layer)
    def compileModel(self): self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=['accuracy'])
    def fitModel(X, Y, epochs, batch_size): self.model.fit(X, Y, epochs=epochs, batch_size=batch_size, verbose=2)
class Loss:        pass
class Optimizer:   pass
class Layer:
    def __init__(self, units, activation, kernel_initializer, bias_initializer):
        self.units              = units
        self.activation         = activation
        self.kernel_initializer = kernel_initializer
        self.bias_initializer   = bias_initializer
    def createLayer(self): self.layer = Dense(self.units, activation=self.activation, kernel_initializer=self.kernel_initializer, bias_initializer=self.bias_initializer)
        
class Activation:  pass

pset = gp.PrimitiveSetTyped("MAIN", (), Model)

pset.addPrimitive(Model, (list, Loss, Optimizer, Activation, Initializer, Initializer), Model)
pset.addPrimitive(lambda x: x, (int,), int, name="id_int")

pset.addPrimitive(lambda l, e: l + [e], (list, Layer), Layer, name="append")
pset.addTerminal([], list)

# TODO
pset.addEphemeralConstant("rand10", lambda: randint(-10, 10), int)

pset.addTerminal(Zeros(), Initializer)
pset.addTerminal(Ones(),  Initializer)
pset.addEphemeralConstant("const_init", lambda: Constant       (
    value       =choice(None, random())), Initializer)
pset.addEphemeralConstant("rn_init",    lambda: RandomNormal   (
    mean        =choice(None, random()),
    stddev      =choice(None, random())), Initializer)
pset.addEphemeralConstant("ru_init",    lambda: RandomUniform  (
    minval      =choice(None, random()),
    maxval      =choice(None, random())), Initializer)
pset.addEphemeralConstant("tn_init",    lambda: TruncatedNormal(
    mean        =choice(None, random()),
    stddev      =choice(None, random())), Initializer)
pset.addEphemeralConstant("vs_init",    lambda: VarianceScaling(
    scale       =choice(None, random()),
    mode        =choice(None, choice(["fan_in", "fan_out", "fan_avg"])),
    distribution=choice(None, choice("normal", "uniform"))), Initializer)
pset.addEphemeralConstant("o_init",     lambda: Orthogonal     (
    gain        =choice(None, random())), Initializer)
pset.addEphemeralConstant("i_init",     lambda: Identity(
    gain        =choice(None, random())), Initializer)
# TODO

pset.addEphemeralConstant("loss",       lambda: choice('mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_logarithmic_error', 'squared_hinge', 'hinge', 'categorical_hinge', 'logcosh'), Loss)
# TODO

pset.addEphemeralConstant("sgd_opt",    lambda: SGD(
    lr      =choice(None, random()),
    momentum=choice(None, random()),
    decay   =choice(None, random()),
    nesterov=choice(None, bool(randbit(1)))), Optimizer)
pset.addEphemeralConstant("rms_opt",    lambda: RMSprop(
    lr      =choice(None, random()),
    rho     =choice(None, random()),
    epsilon =choice(None, random()),
    decay   =choice(None, random())),         Optimizer)
pset.addEphemeralConstant("adag_opt",   lambda: Adagrad(
    lr      =choice(None, random()),
    epsilon =choice(None, random()),
    decay   =choice(None, random())),         Optimizer)
# TODO

def softmaxHelper(axis): return lambda x: softmax(x, axis)
pset.addEphemeralConstant('softmax', lambda: softmaxHelper(randint()), Activation)
def eluHelper(alpha):    return lambda x: elu    (x, alpha)
pset.addEphemeralConstant('elu',     lambda: eluHelper(random()),      Activation)
pset.addTerminal(selu,     Activation)
pset.addTerminal(softplus, Activation)
pset.addTerminal(softsign, Activation)
# TODO

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def fitness_function(individual):
    # Transform the tree expression in a callable function
    model = toolbox.compile(expr=individual)
    print(model.test)
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
#toolbox.register("mutate", gp.mutEphemeral, mode="one")
#toolbox.register("mutate", gp.mutEphemeral, mode="all")
toolbox.register("mutate", gp.mutInsert, pset=pset)
#toolbox.register("mutate", gp.mutSemantic, pset=pset)

#MAX_HEIGHT = 17
MAX_HEIGHT = 90
toolbox.decorate("mate", gp.staticLimit(operator.attrgetter('height'), MAX_HEIGHT))
toolbox.decorate("mutate", gp.staticLimit(operator.attrgetter('height'), MAX_HEIGHT))

def main():
    print("generate a neural network")
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
    print("%s => %s => %s" % (hof[0], str(l), getS(l)))

    return pop, stats, hof
if __name__ == "__main__": main()
