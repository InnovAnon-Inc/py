import random
import operator
import csv
import itertools

import numpy

from random import randint, getrandbits, random, choice

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

class Start:
	def __init__(self, pt, move1, move2, move3, move4, move5):
		assert pt is not None
		assert move1 is not None
		assert move2 is not None
		assert move3 is not None
		assert move4 is not None
		assert move5 is not None
		self.pt = pt
		self.move1 = move1
		self.move2 = move2
		self.move3 = move3
		self.move4 = move4
		self.move5 = move5
	def __repr__(self):
		return "Start(%s, %s, %s, %s, %s, %s)" % (self.pt, self.move1, self.move2, self.move3, self.move4, self.move5)
	__str__ = __repr__
class Move:
	def __init__(self, direction, distance):
		assert direction is not None
		assert distance  is not None
		self.direction = direction
		self.distance  = distance
	def __repr__(self):
		return "Move(%s, %s)" % (self.direction, self.distance)
	__str__ = __repr__
class Direction:
	N  = 0
	NE = 1
	E  = 2
	SE = 3
	S  = 4
	SW = 5
	W  = 6
	NW = 7
	#def __repr__(self):
		
class Point:
	def __init__(self, x, y):
		assert x is not None
		assert y is not None
		self.x = x
		self.y = y
	def __repr__(self):
		return "Point(%s, %s)" % (self.x, self.y)
	__str__ = __repr__
class Distance:
	def __init__(self, val):
		assert val is not None
		self.val = val
	def __repr__(self):
		return "Distance(%s)" % self.val
	__str__ = __repr__

# defined a new primitive set for strongly typed GP
pset = gp.PrimitiveSetTyped("MAIN", (), Start)

pset.addPrimitive(Start,  (Point, Move, Move, Move, Move, Move), Start)

pset.addPrimitive(lambda x: x, (Move,),      Move,      name="moveid")
pset.addPrimitive(lambda x: x, (Point,),     Point,     name="ptid")

pset.addEphemeralConstant("randpt", lambda: Point(randint(0, 10), randint(0, 10)), Point)
pset.addEphemeralConstant("randmv", lambda: Move(
	choice([Direction.N, Direction.NE, Direction.E, Direction.SE, Direction.S, Direction.SW, Direction.W, Direction.NW]),
	Distance(randint(1, 5))), Move)
pset.context['Move'] = Move
pset.context['Start'] = Start
pset.context['Point'] = Point
pset.context['Direction'] = Direction
pset.context['Distance'] = Distance

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def fitness_function(individual):
	k = toolbox.compile(expr=individual)
	print(k)
	board = [
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 1, 1, 1, 0, 0],
		[0, 0, 1, 1, 1, 0, 0],
		[0, 0, 1, 1, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0]]
	y = k.pt.y
	x = k.pt.x
	for m in [k.move1, k.move2, k.move3, k.move4, k.move5]:
		for _ in range(0, m.distance.val):
			if y >= 0 and y < len(board) and x >= 0 and x < len(board[y]):
				board[y][x] = 0
			if   m.direction in [Direction.N, Direction.NE, Direction.NW]:
				y = y - 1
			elif m.direction in [Direction.S, Direction.SE, Direction.SW]:
				y = y + 1
			if   m.direction in [Direction.E, Direction.NE, Direction.SE]:
				x = x + 1
			elif m.direction in [Direction.W, Direction.NW, Direction.SW]:
				x = x - 1
	return -sum(sum(r) for r in board),
    
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

    k = hof[0]
    k = toolbox.compile(expr=k)
    print(k)
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]
    y = k.pt.y
    x = k.pt.x
    for m in [k.move1, k.move2, k.move3, k.move4, k.move5]:
        for _ in range(0, m.distance.val):
            if y >= 0 and y < len(board) and x >= 0 and x < len(board[y]):
                board[y][x] = 0
            if   m.direction in [Direction.N, Direction.NE, Direction.NW]:
                y = y - 1
            elif m.direction in [Direction.S, Direction.SE, Direction.SW]:
                y = y + 1
            if   m.direction in [Direction.E, Direction.NE, Direction.SE]:
                x = x + 1
            elif m.direction in [Direction.W, Direction.NW, Direction.SW]:
                x = x - 1
            for row in board:
            	print(row)
            print()
    
    #print("%s => %s" % (hof[0], str(toolbox.compile(expr=hof[0]))))

    return pop, stats, hof

if __name__ == "__main__": main()

