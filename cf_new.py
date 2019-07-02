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


def autofdo(): pass
def pgo():     pass





"""
class CF:
    def __init__(self, profiling, packing, flags):
        self.profiling = profiling
        self.packing   = packing
        self.flags     = flags
    def __repr__(self): return 'CF(%s, %s, %s)' % (self.profiling, self.packing, self.flags)
"""
"""
class Profiling:
    def __init__(self, val):
        #print("val=%s" % val)
        self.val = val
    #def __str__ (self): return str(self.val)
    #def __repr__(self): #return 'Profiling("%s")' % self.val if self.val else 'Profiling(None)'
    #    return 'Profiling(%s)' % self.val
"""
"""
class Flag:
    def __init__(self, val): self.val = val
    #def __str__ (self): return str(self.val)
    def __repr__(self): #return 'Flag("%s")' % self.val if self.val else 'Flag(None)'
        return 'Flag(%s)' % self.val
"""



class Profiling:
    values = [None, 'autofdo', 'pgo']
profiling = Profiling()

pset = gp.PrimitiveSetTyped("MAIN", (), Profiling)

for value in profiling.values:
    pset.addTerminal(value, Profiling, name=str(value))


pset.addPrimitive(lambda x: x, (Profiling,), Profiling, name="id")









"""

    def __init__(self, fuck):
        self.fuck = fuck
    def __repr__(self): return 'Profiling(%s)' % repr(self.fuck)

pset = gp.PrimitiveSetTyped("MAIN", (), Profiling)

#pset.addPrimitive(Profiling, (int,), Profiling)
pset.addPrimitive(lambda x: x, (Profiling,), Profiling, name="id")

#pset.addEphemeralConstant("rand10", lambda: choice([None, 0, 1, 2]), int)

pset.addEphemeralConstant("prof", lambda: Profiling(choice([None, 0, 1, 2])), Profiling)
"""

#pset = gp.PrimitiveSetTyped("MAIN", (), CF)
#pset = gp.PrimitiveSetTyped("MAIN", (), Profiling)

#pset.addPrimitive(CF, (Profiling, bool, list), CF)
#pset.addPrimitive(CF, (Profiling, bool, list), CF)
#pset.addPrimitive(CF, (Profiling, bool, bool), CF)

#pset.addPrimitive(lambda l, e: l + [e], (list, Flag), list, name="append")
#pset.addPrimitive(lambda l, k: l + k,   (list, list), list, name="concat")
#pset.addTerminal([], list)

#pset.addPrimitive(lambda x: x, (Profiling,), Profiling, name="prof_id")
#pset.addPrimitive(lambda x: x, (bool,),      bool,      name="bool_id")
#pset.addPrimitive(lambda x: x, (list,),      list,      name="list_id")

#pset.addEphemeralConstant("profiling", lambda: Profiling(choice([None, 'autofdo', 'pgo'])), Profiling)
#pset.addEphemeralConstant("packing",   lambda: bool(getrandbits(1)),          bool)
# TODO generate a subset
"""
pset.addEphemeralConstant("flag1",     lambda: Flag(choice([
    '-faggressive-loop-optimizations',
    '-fassociative-math',
    '-fauto-inc-dec',
    '-fbranch-target-load-optimize',
    '-fbranch-target-load-optimize2',
    '-fbtr-bb-exclusive',
    '-fcaller-saves',
    '-fcheck-data-deps',
    '-fcombine-stack-adjustments',
    '-fconserve-stack',
    '-fcompare-elim',
    '-fcprop-registers',
    '-fcrossjumping',
    '-fcse-follow-jumps',
    '-fcse-skip-blocks',
    '-fcx-fortran-rules',
    '-fcx-limited-range',
    '-fdata-sections',
    '-fdce',
    '-fdelayed-branch',
    '-fdelete-null-pointer-checks',
    '-fdevirtualize',
    '-fdevirtualize-speculatively',
    '-fdevirtualize-at-ltrans',
    '-fdse',
    '-fearly-inlining',
    '-fipa-sra',
    '-fexpensive-optimizations',
    '-ffat-lto-objects',
    '-ffast-math',
    '-ffinite-math-only',
    '-ffloat-store',
    '-fforward-propagate',
    '-ffunction-sections',
    '-fgcse',
    '-fgcse-las',
    '-fgcse-lm',
    '-fgraphite-identity',
    '-fgcse-sm',
    '-fhoist-adjacent-loads',
    '-fif-conversion',
    '-fif-conversion2',
    '-findirect-inlining',
    '-finline-functions-called-once',
    '-finline-small-functions',
    '-fipa-cp-alignment',
    '-fipa-pta',
    '-fipa-profile',
    '-fipa-pure-const',
    '-fipa-reference',
    '-fipa-icf',
    '-fira-hoist-pressure',
    '-fira-loop-pressure',
    '-fno-ira-share-save-slots',
    '-fno-ira-share-spill-slots',
    '-fisolate-erroneous-paths-dereference',
    '-fisolate-erroneous-paths-attribute',
    '-fivopts',
    '-fkeep-inline-functions',
    '-fkeep-static-consts',
    '-flive-range-shrinkage',
    '-floop-block',
    '-floop-interchange',
    '-floop-strip-mine',
    '-floop-unroll-and-jam',
    '-floop-nest-optimize',
    '-floop-parallelize-all',
    '-flra-remat',
    '-flto',
    '-fmerge-all-constants',
    '-fmerge-constants',
    '-fmodulo-sched',
    '-fmodulo-sched-allow-regmoves',
    '-fmove-loop-invariants',
    '-fno-branch-count-reg',
    '-fno-defer-pop',
    '-fno-function-cse',
    '-fno-guess-branch-probability',
    '-fno-inline',
    '-fno-math-errno',
    '-fno-peephole',
    '-fno-peephole2',
    '-fno-sched-interblock',
    '-fno-sched-spec',
    '-fno-signed-zeros',
    '-fno-toplevel-reorder',
    '-fno-trapping-math',
    '-fno-zero-initialized-in-bss',
    '-fomit-frame-pointer',
    '-foptimize-sibling-calls',
    '-fpartial-inlining',
    '-fprefetch-loop-arrays',
    '-fprofile-correction',
    '-fprofile-reorder-functions',
    '-freciprocal-math',
    '-free',
    '-frename-registers',
    '-freorder-blocks',
    '-freorder-blocks-and-partition',
    '-freorder-functions',
    '-frerun-cse-after-loop',
    '-freschedule-modulo-scheduled-loops',
    '-frounding-math',
    '-fsched2-use-superblocks',
    '-fsched-pressure',
    '-fsched-spec-load',
    '-fsched-spec-load-dangerous',
    '-fsched-group-heuristic',
    '-fsched-critical-path-heuristic',
    '-fsched-spec-insn-heuristic',
    '-fsched-rank-heuristic',
    '-fsched-last-insn-heuristic',
    '-fsched-dep-count-heuristic',
    '-fschedule-fusion',
    '-fschedule-insns',
    '-fschedule-insns2',
    '-fsection-anchors',
    '-fselective-scheduling',
    '-fselective-scheduling2',
    '-fsel-sched-pipelining',
    '-fsel-sched-pipelining-outer-loops',
    '-fsemantic-interposition',
    '-fshrink-wrap',
    '-fsignaling-nans',
    '-fsingle-precision-constant',
    '-fsplit-ivs-in-unroller',
    '-fsplit-wide-types',
    '-fssa-phiopt',
    '-fstdarg-opt',
    '-fstrict-aliasing',
    '-fstrict-overflow',
    '-fthread-jumps',
    '-ftree-bit-ccp',
    '-ftree-builtin-call-dce',
    '-ftree-ccp',
    '-ftree-ch',
    '-ftree-coalesce-inline-vars',
    '-ftree-coalesce-vars',
    '-ftree-copy-prop',
    '-ftree-copyrename',
    '-ftree-dce',
    '-ftree-dominator-opts',
    '-ftree-dse',
    '-ftree-forwprop',
    '-ftree-fre',
    '-ftree-loop-if-convert',
    '-ftree-loop-if-convert-stores',
    '-ftree-loop-im',
    '-ftree-phiprop',
    '-ftree-loop-distribution',
    '-ftree-loop-ivcanon',
    '-ftree-loop-linear',
    '-ftree-loop-optimize',
    '-ftree-loop-vectorize',
    '-ftree-pre',
    '-ftree-partial-pre',
    '-ftree-pta',
    '-ftree-reassoc',
    '-ftree-sink',
    '-ftree-slsr',
    '-ftree-sra',
    '-ftree-switch-conversion',
    '-ftree-tail-merge',
    '-ftree-ter',
    '-ftree-vrp',
    '-funit-at-a-time',
    '-funroll-all-loops',
    '-funsafe-loop-optimizations',
    '-funsafe-math-optimizations',
    '-fipa-ra',
    '-fvariable-expansion-in-unroller',
    '-fvect-cost-model',
    '-fweb',
    '-fwhole-program',
    '-fwpa',
    '-fuse-linker-plugin'
])), Flag)
pset.addEphemeralConstant("flag2",     lambda: Flag(choice([None, '-falign-functions', '-falign-functions=%s' % choice([8, 16, 24, 32, 40, 48, 56, 64])])), Flag)
pset.addEphemeralConstant("flag3",     lambda: Flag(choice([None, '-falign-jumps',     '-falign-jumps=%s'     % choice([8, 16, 24, 32, 40, 48, 56, 64])])), Flag)
pset.addEphemeralConstant("flag4",     lambda: Flag(choice([None, '-falign-loops',     '-falign-loops=%s'     % choice([8, 16, 24, 32, 40, 48, 56, 64])])), Flag)
pset.addEphemeralConstant("flag5",     lambda: Flag(choice([None, '-finline-limit=%s'     % choice([100, 300, 600, 900, 1200])])), Flag)
pset.addEphemeralConstant("flag6",     lambda: Flag(choice([None, '-fexcess-precision=%s' % choice(['fast', 'standard'])])),       Flag)
pset.addEphemeralConstant("flag7",     lambda: Flag(choice([None, '-ffp-contract=%s'      % choice(['fast', 'on', 'off'])])),      Flag)
pset.addEphemeralConstant("flag8",     lambda: Flag(choice([None, '-fira-algorithm=%s'    % choice(['CB', 'priority'])])),         Flag)
pset.addEphemeralConstant("flag9",     lambda: Flag(choice([None, '-fira-region=%s'       % choice(['all', 'mixed', 'one'])])),    Flag)
pset.addEphemeralConstant("flag10",    lambda: Flag(choice([None, '-flto-compression-level=%s' % randint(0, 9)])),               Flag)
pset.addEphemeralConstant("flag11",    lambda: Flag(choice([None, '-flto-partition=%s'    % choice(['balanced', 'none', 'max', '1to1', 'one'])])), Flag)
pset.addEphemeralConstant("flag12",    lambda: Flag(choice([None, '-fsched-stalled-insns-dep', '-fsched-stalled-insns-dep=%s' % randint(0, 3)])), Flag)
pset.addEphemeralConstant("flag13",    lambda: Flag(choice([None, '-fsched-stalled-insns', '-fsched-stalled-insns=%s' % randint(0, 3)])), Flag)
pset.addEphemeralConstant("flag14",    lambda: Flag(choice([None, '-fstack-protector', '-fstack-protector-all', '-fstack-protector-strong', '-fstack-protector-explicit'])), Flag)
pset.addEphemeralConstant("flag15",    lambda: Flag(choice([None, '-ftree-parallelize-loops=%s' % randint(1, 24)])), Flag)
pset.addEphemeralConstant("flag16",    lambda: Flag(choice([None, '-O', '-O0', '-O1', '-O2', '-O3', '-Os', '-Ofast', '-Og'])), Flag)
"""

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
    #print(cf.fuck)
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
