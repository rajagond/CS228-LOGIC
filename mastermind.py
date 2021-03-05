#!/usr/bin/python3

from z3 import *
import itertools

n = 8
k = 3
coun = 0
vs = []

# write function that encodes that exactly one variable is one
def sum_to_one( ls ):
    at_least_one = Or( ls )
    at_most_one_list = []
    for pair in itertools.combinations( ls, 2):
        l1 = pair[0]
        l2 = pair[1]
        at_most_one_list.append( Or( Not(l1), Not(l2) ) )
    at_most_one = And( at_most_one_list  )
    return And( at_least_one, at_most_one )

# mastermind.initialize(n,k)
def initialize(x,y):
    global n, k, coun, vs
    n = x
    k = y
    coun = 0
    # print(n, " ",k, " ", coun)

    # declare variables 
    vs = [  [Bool("e_{}_{}".format(i,j))  for j in range(n)] for i in range(k)]

    # call the function
    F = And([sum_to_one( vs[i] ) for i in range(k)])

    # print(F)
    # add the formula in the solver
    s.add( F )


prev = []
#  mastermind.get_second_player_move()
def get_second_player_move():
    res = []
    global prev
    # print(prev)
    # check sat value
    result = s.check()

    if result == sat:
        # get satisfying model
        m = s.model()
        for i in range(k):
            for j in range(n):
                if is_true( m[vs[i][j]] ):
                    res.append(j)
        prev = res[:]
    else:
        # print("unsat")
        raise Exception("May be crossed certain limit of unreliability")
    return res

# mastermind.put_first_player_response( red, white )
def put_first_player_response( red, white ):
    global coun
    if not prev:
        raise Exception("something bad happen in reading previous feedback")
    else:
        l = [ vs[i][prev[i]] for i in range(k)]

        w = [ Or([vs[j][prev[i]] for j in range(k)]) for i in range(k)]

        Feedback = And(PbEq([(x,1) for x in l], red), PbGe([(w[i],1) for i in range(len(w))], white) )
        var = Bool("x_{}".format(coun))
        s.add( Or(Feedback, Not(var)))
        s.add_soft(var)
        coun = coun + 1

# construct Z3 solver
s = Optimize()