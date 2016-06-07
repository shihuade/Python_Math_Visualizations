# coding = utf-8

import random
import cairo
from itertools import product

def grid(*size):
    
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
    

def ust(graph):
    
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
    
def draw_ust(*size):
    m,n,W,H = size
    G = grid(m,n)
    T = ust(G)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    cr.scale(W/(m+1.0), -H/(n+1.0))
    cr.translate(1,-n)
    cr.set_source_rgb(0.2,0.2,0.2)
    cr.paint()
    cr.set_line_cap(2)

    for v, w in T.items():
        a, b = v
        if w:
            c, d = w
            cr.set_source_rgb(1,1,1)
            cr.set_line_width(0.5)
            cr.move_to(a,b)
            cr.line_to(c,d)
            cr.stroke()
    surface.write_to_png("Wilson_Uniform_Spanning_Tree.png")

draw_ust(120,90,800,600)
