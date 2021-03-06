# coding = utf-8

import random
import cairo
from itertools import product
from collections import deque

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
            
        # can you see where is the "loop erasing"?
        # the trick is when you are visiting a vertex twice, the dict "parent" only records the second visit    
        
        v = vertex
        while v not in tree:
            tree.add(v)
            v = parent[v]
    return parent

def tree_to_graph(tree):
    """
    This step is for the bfs animation
    """
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

def find_path(gridsize, imagesize, borderwidth=3):
    
    m, n = gridsize
    W, H = imagesize
    g = grid_graph(m,n)
    T = uniform_spanning_tree(g)
    G = tree_to_graph(T)
    
    start = (0,0)
    end = (m-1,n-1)
    # use a dict to record each step
    visitedfrom = dict()
    count = 0
    
    for child, parent in bfs(G, start):
        visitedfrom[child] = parent
        if child == end or count % 50 == 0:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            cr = cairo.Context(surface)
            
            # borderwidth is the distance between the border of the maze and the edge of the page
            # the coordinate system of cairo has its (0,0) at the upperleft corner
            # we need to transform it to the lowerleft corner
            cr.scale(W/(m-1.0+2.0*borderwidth),-H/(n-1.0+2.0*borderwidth))
            cr.translate(borderwidth,-n-borderwidth+1)
            
            # paint the page "white"
            cr.set_source_rgb(1,1,1)
            cr.paint()
            cr.set_line_cap(2)
            
            # paint the background color of the maze "black"
            cr.rectangle(0,0,m-1,n-1)
            cr.set_source_rgb(0,0,0)
            cr.fill_preserve()
            cr.set_line_width(2)
            cr.stroke()
            
            # draw maze in white
            for v, w in T.items():
                if w:
                    cr.set_source_rgb(1,1,1)
                    cr.set_line_width(0.5)
                    cr.move_to(v[0],v[1])
                    cr.line_to(w[0],w[1])
                    cr.stroke()
                    
            # draw visited cells in green
            for a, b in visitedfrom.items():
                if b:
                    cr.move_to(a[0],a[1])
                    cr.line_to(b[0],b[1])
                    cr.set_source_rgb(0,1,0)
                    cr.set_line_width(0.5)
                    cr.stroke()
                    
            # if a path is found, then draw it red
            if child == end:
                path = [end]
                w = end
                while w != start:
                    w = visitedfrom[w]
                    path.append(w)
                for i in range(len(path)-1):
                    cr.move_to(path[i][0], path[i][1])
                    cr.line_to(path[i+1][0], path[i+1][1])
                    cr.set_source_rgb(1,0,0)
                    cr.set_line_width(0.5)
                    cr.stroke()
                surface.write_to_png("maze%03d.png"%(int(count/50.0+0.5)))
                # return the path from "start" to "end"
                return path[::-1]

            surface.write_to_png("maze%03d.png"%(count/50))
        count += 1

find_path(gridsize, imagesize)
