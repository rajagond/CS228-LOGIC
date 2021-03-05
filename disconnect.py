from z3 import *
from collections import defaultdict

def all_path(u, d, visited, path,graph,pathf):
    visited[u]= True
    path.append(u)
    if u == d:
        pathf.append(copy.deepcopy(path))
    else:
        for i in graph[u]:
            if visited[i]== False:
                all_path(i, d, visited, path,graph,pathf)
    path.pop() 
    visited[u]= False   


def find_minimal(graph, s, t):

        vars = []
        for edge in graph:
            if(edge[0]<edge[1]):
                vars.append(Bool ("e_{}_{}".format(edge[0],edge[1]) ))
            else:
                vars.append(Bool ("e_{}_{}".format(edge[1],edge[0]) ))

        graph2 = defaultdict(list)
        visited = defaultdict(bool)

        for e in graph:
            graph2[e[0]].append(e[1])  
            graph2[e[1]].append(e[0])
            visited[e[1]] = False
            visited[e[0]] = False

        path=[]
        pathf=[]
        all_path(s, t, visited, path,graph2,pathf)
        mnslv = []

        for paths in pathf:
            p = []
            for v in range(len(paths)-1):
                if(paths[v]<paths[v+1]):
                    p.append(Bool ("e_{}_{}".format(paths[v],paths[v+1]) ) )
                else:
                    p.append(Bool ("e_{}_{}".format(paths[v+1],paths[v]) ) )
            mnslv.append(Not(And(p)))

        for i in reversed(range(len(vars))):
            s = Solver()
            s.add(And(mnslv))
            s.add(PbEq([(x,1) for x in vars],i))
            if(s.check()==sat):
                return len(vars)-i

