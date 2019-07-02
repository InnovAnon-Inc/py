import random
import operator
import csv
import itertools

import numpy

from random import randint, getrandbits

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

"""
class Ints:
    def __init__(self, a, b=None):
        self.a, self.b = a, b
    def toList():
        if   self.a is int: A = [self.a]
        elif not self.a:    A = []
        else:               A = self.a.toList()

        if   self.b is int: B = [self.b]
        elif not self.b:    B = []
        else:               B = self.b.toList()

        return A + B

# defined a new primitive set for strongly typed GP
pset = gp.PrimitiveSetTyped("MAIN", (), Ints)

##pset.addPrimitive(lambda x:    return x, (Ints,),      Ints)
#pset.addPrimitive(lambda x, y: Ints(x, y), (Ints, Ints), Ints)
#pset.addPrimitive(lambda x, y: Ints(x, y), (int,  int),  Ints)
#pset.addPrimitive(lambda x:    Ints(x),    (Int,),       Ints)
#pset.addPrimitive(lambda x:    Ints(x),    (int,),       Ints)

pset.addPrimitive(lambda x, y: Ints(x, y), (Ints, int), Ints, name='cons2')
pset.addPrimitive(lambda y:    Ints(y),    (int,),      Ints, name='cons1')

pset.addEphemeralConstant("rand10", lambda: randint(0, 11), int)
"""

# defined a new primitive set for strongly typed GP
pset = gp.PrimitiveSetTyped("MAIN", (), int)

# boolop = And | Or 
#pset.addPrimitive(operator.and_, (bool, bool), bool)
#pset.addPrimitive(operator.or_,  (bool, bool), bool)

#operator = Add | Sub | Mult | Div | Mod | Pow | LShift 
#                 | RShift | BitOr | BitXor | BitAnd | FloorDiv
pset.addPrimitive(operator.add,      (int, int), int)
pset.addPrimitive(operator.sub,      (int, int), int)
pset.addPrimitive(operator.mul,      (int, int), int)
pset.addPrimitive(operator.floordiv, (int, int), int)
pset.addPrimitive(operator.mod,      (int, int), int)
pset.addPrimitive(operator.lshift,   (int, int), int)
pset.addPrimitive(operator.rshift,   (int, int), int)
pset.addPrimitive(operator.xor,      (int, int), int)

pset.addPrimitive(min, (int, int), int)
pset.addPrimitive(max, (int, int), int)
#pset.addPrimitive(pow, (int, int), int)

#pset.addPrimitive(lambda cond, conseq, alt: conseq if cond else alt, (bool, int, int), int, name="if_else_expr")

# cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
#pset.addPrimitive(operator.lt, (int, int), bool)
#pset.addPrimitive(operator.le, (int, int), bool)
#pset.addPrimitive(operator.eq, (int, int), bool)
#pset.addPrimitive(operator.ne, (int, int), bool)
#pset.addPrimitive(operator.ge, (int, int), bool)
#pset.addPrimitive(operator.gt, (int, int), bool)

# unaryop = Invert | Not | UAdd | USub
#pset.addPrimitive(operator.not_,   (bool,), bool)
pset.addPrimitive(operator.abs,    (int,),  int)
pset.addPrimitive(operator.invert, (int,), int)
pset.addPrimitive(operator.neg,    (int,), int)
pset.addPrimitive(operator.pos,    (int,), int)

#pset.addPrimitive(lambda q, d: q // d if d else 0, (int, int), int, name="safe_div")
#pset.addPrimitive(lambda q, d: q % d if d else 0, (int, int), int, name="safe_mod")
#pset.addPrimitive(lambda a, s: a << abs(s), (int, int), int, name="safe_lshift")
#pset.addPrimitive(lambda a, s: a >> abs(s), (int, int), int, name="safe_rshift")

#pset.addTerminal(False, bool)
#pset.addTerminal(True, bool)

#pset.addEphemeralConstant("randbool", lambda: bool(getrandbits(1)), bool)





#pset.addEphemeralConstant("rand10", lambda: randint(0, 11), int)
pset.addEphemeralConstant("rand10", lambda: randint(-(1<<32), +(1<<32)), int)
#pset.addEphemeralConstant("rand10", lambda: randint(-(1<<10), +(1<<10)) ^ ord('A'), int)
#pset.addEphemeralConstant("rand10", lambda: randint(0, 11), int)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def fitness_function(individual):
    # Transform the tree expression in a callable function
    try:                      i = toolbox.compile(expr=individual)
    except OverflowError:     return float("-inf"),
    except ZeroDivisionError: return float("-inf"),
    except ValueError:        return float("-inf"),
    #l = i.toList()
    #S = sum(l)
    S = i
    #L = len(l)
    L = len(individual)
    a = 42
    try:                  e = abs(S - a) / a * 10
    except OverflowError: return float("-inf"),
    w = abs(L - 3) / 3 * .1
    #print(individual, i, - (1 + e) * (1 + w))
    return - (1 + e) * (1 + w),
    
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
    print("generate an expression which yields 42")

    #random.seed(10)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 30, stats, halloffame=hof)

    print("%s => %s" % (hof[0], str(toolbox.compile(expr=hof[0]))))

    return pop, stats, hof

if __name__ == "__main__": main()

"""
pset.addPrimitive(operator.lambda, (arguments, expression), function)
pset.addPrimitive(

# boolop = And | Or 
pset.addPrimitive(operator.and_, (bool, bool), bool)
pset.addPrimitive(operator.or_,  (bool, bool), bool)

#operator = Add | Sub | Mult | Div | Mod | Pow | LShift 
#                 | RShift | BitOr | BitXor | BitAnd | FloorDiv
pset.addPrimitive(operator.add,      (int, int), int)
pset.addPrimitive(operator.sub,      (int, int), int)
pset.addPrimitive(operator.mul,      (int, int), int)
#pset.addPrimitive(operator.div,      (int, int), float)
#pset.addPrimitive(operator.floordiv, (int, int), int)
#pset.addPrimitive(operator.truediv,  (int, int), float)
pset.addPrimitive(operator.lshift,   (int, int), int)
pset.addPrimitive(operator.rshift,   (int, int), int)
#pset.addPrimitive(operator.mod,      (int, int), int)
pset.addPrimitive(operator.xor,      (int, int), int)
#pset.addPrimitive(operator.concat,   (sequence, sequence), sequence)

# unaryop = Invert | Not | UAdd | USub
pset.addPrimitive(operator.not_,   (bool,), bool)
pset.addPrimitive(operator.abs,    (int,),  int)
pset.addPrimitive(operator.index,  (object,), int)
pset.addPrimitive(operator.invert, (object,), object)
pset.addPrimitive(operator.neg,    (object,), object)
pset.addPrimitive(operator.pos,    (object,), object)

#pset.addPrimitive(int,             (str,),    int)
#pset.addPrimitive(int,             (float,),  int)

# cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn
pset.addPrimitive(operator.lt, (int, int), bool)
pset.addPrimitive(operator.le, (int, int), bool)
pset.addPrimitive(operator.eq, (int, int), bool)
pset.addPrimitive(operator.ne, (int, int), bool)
pset.addPrimitive(operator.ge, (int, int), bool)
pset.addPrimitive(operator.gt, (int, int), bool)

# terminals
pset.addEphemeralConstant("rand100", lambda: random.random() * 100, float)
pset.addTerminal(False, bool)
pset.addTerminal(True, bool)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

sample_io = {
    (0, 0) : 1, (1, 0) : 1, (2, 0) : 1, (3, 0) :  1, (4, 0) :  1,
    (0, 1) : 0, (1, 1) : 1, (2, 1) : 2, (3, 1) :  3, (4, 1) :  4,
    (0, 2) : 0, (1, 2) : 1, (2, 2) : 4, (3, 2) :  9, (4, 2) : 16,
    (0, 3) : 0, (1, 3) : 1, (2, 3) : 8, (3, 3) : 27, (4, 3) : 64
}
print(len(sample_io))

def evalSpambase(individual):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Randomly sample 400 mails in the spam database
    #spam_samp = random.sample(spam, 400)
    # Evaluate the sum of correctly identified mail as spam
    #result = sum(bool(func(*mail[:57])) is bool(mail[57]) for mail in spam_samp)
    cnt = 0
    try:
        for args in sample_io:
            ao = func(*args)
            eo = sample_io[args]
            if eo == ao: cnt = cnt + 1
        return cnt,
    except: return -1,
    
toolbox.register("evaluate", evalSpambase)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    random.seed(10)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof)

    print(hof[0])
    print(str(toolbox.compile(expr=hof[0])))

    return pop, stats, hof

if __name__ == "__main__": main()
"""
