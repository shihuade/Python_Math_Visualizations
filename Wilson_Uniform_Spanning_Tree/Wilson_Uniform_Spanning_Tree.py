# coding = utf-8

import random
import cairo
from itertools import product

gridsize = (80, 60)
imagesize = (800, 600)

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
    
def draw_random_maze(gridsize, imagesize, linewidth=0.5, borderwidth=3):
    m, n = gridsize
    W, H = imagesize
    grid = grid_graph(m,n)
    T = uniform_spanning_tree(grid)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    cr.scale(W/(m-1.0+2.0*borderwidth),-H/(n-1.0+2.0*borderwidth))
    cr.translate(borderwidth,-n-borderwidth+1)
    cr.set_source_rgb(1,1,1)
    cr.paint()
    cr.set_line_cap(2)
    cr.rectangle(0,0,m-1,n-1)
    cr.set_source_rgb(0,0,0)
    cr.fill_preserve()
    cr.set_line_width(4*linewidth)
    cr.stroke()
    
    for v, w in T.items():
        if w:
            cr.set_source_rgb(1,1,1)
            cr.set_line_width(linewidth)
            cr.move_to(v[0],v[1])
            cr.line_to(w[0],w[1])
            cr.stroke()
    surface.write_to_png("Wilson_Uniform_Spanning_Tree.png")
    
draw_random_maze(gridsize, imagesize)
