# coding = utf-8

import random
import cairo
from itertools import product

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
    
def draw_random_maze(m,n,W,H,linewidth=0.5,border=3):
    g = grid_graph(m,n)
    T = uniform_spanning_tree(g)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    cr.scale(W/(m-1.0+2.0*border),-H/(n-1.0+2.0*border))
    cr.translate(border,-n-border+1)
    cr.set_source_rgb(1,1,1)
    cr.paint()
    cr.set_line_cap(2)
    cr.rectangle(0,0,m-1,n-1)
    cr.set_source_rgb(0,0,0)
    cr.fill_preserve()
    cr.set_line_width(4*linewidth)
    cr.stroke()
    
    for v, w in T.items():
        a, b = v
        if w:
            c, d = w
            cr.set_source_rgb(1,1,1)
            cr.set_line_width(linewidth)
            cr.move_to(a,b)
            cr.line_to(c,d)
            cr.stroke()
    surface.write_to_png("Wilson_Uniform_Spanning_Tree.png")
    
draw_random_maze(80,60,800,600)
