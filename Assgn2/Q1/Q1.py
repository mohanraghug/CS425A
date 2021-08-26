import sys
from itertools import islice  # Useful while parsing the Topology.txt

#################################
## Parse the Topology.txt file ##
#################################

edges = set()
nodes = 0

f = open("Topology.txt", "r")

s = f.readline()
ip = s[:-1]
while s and ip:
    n = int(f.readline()[:-1])
    nodes += 1

    for _ in range(n):
        s = f.readline()[:-1]
        to, cost = s.split('\t')
        cost = float(cost)
        edges.add((ip, to, cost))
        edges.add((to, ip, cost))

    s = f.readline()
    s = f.readline()
    ip = s[:-1]

# Implementation for BellmanFord Algorithm


def bellmanFord(edges, Source, nodes):
    d = {}    # d[Node] is the length of shortest path from Source to Node
    prv = {}
    # prv[Node] contains the node before "Node" in the shortest path from Source to Node
    nxt = {}
    # nxt[Node] contains the node after "Source" in the shortest path from Source to Node

    d[Source] = 0
    prv[Source] = Source

    # Bellman Ford Algorithm
    for _ in range(nodes+2):
        for u, v, cost in edges:
            if u in d.keys() and (v not in d.keys() or d[v] > d[u] + cost):
                # edge Relaxation
                d[v] = d[u] + cost
                prv[v] = u

    # finding nxt[Node] using prv values
    for node in prv.keys():
        at = node
        while prv[at] != Source:
            at = prv[at]
        nxt[node] = at

    return d, nxt


def distanceFinder(source_ip):  # Do something ##
    # source_ip is a string value. eg: '10.1.2.10'
    d, nxt = bellmanFord(edges, source_ip, nodes)
    lst = list(d.keys())
    lst.sort()
    for node in lst:
        print(source_ip, node, float(d[node]), nxt[node], sep=", ")
    print()


def updateRouterCost(router1, router2, d, source_ip):  # Do something ##
    # router1,router2 and source_ip are string values
    # d is an integer value

    # updating the cost of edges from router1 -> router2 and router2 -> router1
    nedges = set()
    for e in edges:
        u, v, cost = e
        if (u == router1 and v == router2) or (u == router2 and v == router1):
            nedges.add((u, v, cost+d))
        else:
            nedges.add((u, v, cost))

    # Running bellman Ford with original and updated set of edges
    d1, nxt1 = bellmanFord(edges, source_ip, nodes)
    d2, nxt2 = bellmanFord(nedges, source_ip, nodes)

    case1 = []
    case2 = []
    for node in d1.keys():
        if d1[node] == d2[node]:
            case1.append(node)
        else:
            case2.append(node)

    case1.sort()
    case2.sort()

    print("Case-1")
    for node in case1:
        print(source_ip, node, float(d2[node]), nxt2[node], sep=", ")

    print("Case-2")
    for node in case2:
        print(source_ip, node, float(d2[node]), nxt2[node], sep=", ")

    print()


def addRouter(newrouter, nlist, ncost, source_ip):  # Do something ##
    # newrouter is a string value. eg: '10.1.6.10'.
    # nlist contains the list of neighbour routers. eg: ['10.1.4.10','10.1.3.10']
    # ncost contains the list of cost values between newrouter and the routers defined in the nlist. eg[3,4]
    # source_ip is a string value. eg: '10.1.2.10'

    # updating edges by adding edges from new node
    nedges = edges.copy()
    for i in range(len(nlist)):
        to = nlist[i]
        cost = float(ncost[i])
        nedges.add((newrouter, to, cost))
        nedges.add((to, newrouter, cost))

    d, nxt = bellmanFord(nedges, source_ip, nodes+1)
    lst = list(d.keys())
    lst.sort()
    for node in lst:
        print(source_ip, node, float(d[node]), nxt[node], sep=", ")

    print()


distanceFinder('10.1.2.10')
updateRouterCost('10.1.3.10', '10.1.4.10', 10, '10.1.2.10')
addRouter('10.1.6.10', ['10.1.5.10', '10.1.4.10'], [3, 4], '10.1.2.10')
