# coding = utf-8

import random
import cairo
from itertools import product
from collections import deque

gridsize = (80, 60)
imagesize = (800, 600)
linewidth = 0.5 
borderwidth = 3

def grid_graph(*size):
    
    def neighbors(v):
        neighborhood = []
        for i in range(len(size)):
            for dx in [-1,1]:
                w = list(v)
                w[i] += dx
                if 0 <= w[i] < size[i]:
                    neighborhood.append(tuple(w))
        return neighborhood
        
    return {v: neighbors(v) for v in product(*map(range, size))}

def uniform_spanning_tree(graph):
    
    root = random.choice(graph.keys())     
    parent = {root: None}
    tree = set([root])
    
    for vertex in graph:
        v = vertex
        while v not in tree:
            neighbor = random.choice(graph[v])
            parent[v] = neighbor
            v = neighbor

        v = vertex
        while v not in tree:
            tree.add(v)
            v = parent[v]
    return parent

def tree_to_graph(tree):
    
    graph = {v: [] for v in tree}
    for vertex in tree:
        parent = tree[vertex]
        if parent is not None:
            graph[vertex].append(parent)
            graph[parent].append(vertex)
    return graph

def bfs(graph, start):
    
    queue = deque()
    queue.append((start, None))
    visited = set([start])
    while queue:
        v, parent = queue.popleft()
        yield v, parent
        for w in graph[v]:
            if w not in visited:
                visited.add(w)
                queue.append((w, v))

def find_path(graph, start, end)
