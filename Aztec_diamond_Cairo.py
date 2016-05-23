#coding = utf-8

# An implementation of the Domino Shuffling Algorithm on Aztec Diamong Graph

import random
import cairo

class aztec_diamond:

    def __init__(self,n):
        """
        use a dict to record a tiling of the graph.
        the keys of the dict are the "coordinates" of the unit squares. 
        each square is specified by its left bottom corner (i,j).
        the j-th row (j from y=-n to y=n-1) contains min(n+1+j,n-j) unit squares
        use "n", "s", "w", "e", "xrepresent the states of the squares.
        """
        
        self.order = n
        self.tile = dict()
        for j in xrange(-n,n):
            k = min(n+1+j,n-j)
            for i in xrange(-k,k):
                self.tile[(i,j)] = 'x'
                
    def delete(self):
        #to find bad blocks, one must search from the boundary.
        n = self.order
        for j in xrange(-n,n):
            k = min(n+1+j,n-j)
            for i in xrange(-k,k):
                try:
                    if ((self.tile[(i,j)]=='n' and self.tile[(i+1,j)]=='n' and self.tile[(i,j+1)]=='s' and self.tile[(i+1,j+1)]=='s') or (self.tile[(i,j)]=='e' and self.tile[(i,j+1)]=='e' and self.tile[(i+1,j)]=='w' and self.tile[(i+1,j+1)]=='w')):
                        self.tile[(i,j)]='x'
                        self.tile[(i+1,j)]='x'
                        self.tile[(i,j+1)]='x'
                        self.tile[(i+1,j+1)]='x'
                except:
                    pass
        return self

    def slide(self):
        n = self.order
        new_board = aztec_diamond(n+1)
        for (i,j) in self.tile.keys():
            if self.tile[(i,j)] == 'n': new_board.tile[(i,j+1)] = 'n'
            if self.tile[(i,j)] == 's': new_board.tile[(i,j-1)] = 's'
            if self.tile[(i,j)] == 'w': new_board.tile[(i-1,j)] = 'w'
            if self.tile[(i,j)] == 'e': new_board.tile[(i+1,j)] = 'e'
        return new_board

    def create(self):
        # to fill the bad blocks, one must also start from the boundary.
        n = self.order
        for j in xrange(-n,n):
            k = min(n+1-j,n-j)
            for i in xrange(-k,k):
                try:
                    if (self.tile[(i,j)] == 'x' and self.tile[(i+1,j)] == 'x' and self.tile[(i,j+1)] == 'x' and self.tile[(i+1,j+1)] == 'x'):
                        if random.random()>0.5:
                            # Here we fill the bdd blocks with a pair of dominoes leaving each other, since a bad block in az(n) will be a good block in az(n+1)

                            self.tile[(i,j)] = 's'
                            self.tile[(i+1,j)] = 's'
                            self.tile[(i,j+1)] = 'n'
                            self.tile[(i+1,j+1)] = 'n'
                        else:
                            self.tile[(i,j)] = 'w'
                            self.tile[(i+1,j)] = 'e'
                            self.tile[(i,j+1)] = 'w'
                            self.tile[(i+1,j+1)] = 'e'
                except:
                    pass
        return self


    def draw(self, size=1024):
        n = self.order
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
        cr = cairo.Context(surface)
        cr.translate(size/2., size/2.)
        d = size/((n+1)*2.0)
        cr.scale(d,d)
        cr.set_source_rgb(1,1,1)
        cr.paint()
        
        for (i,j) in self.tile.keys():
            if (i+j+n)%2 == 1: #a domino is determined by its black square 
                if self.tile[(i,j)] == 'n':
                    cr.rectangle(i-1,j,2,1)
                    cr.set_source_rgb(255,0,0)                    
                if self.tile[(i,j)] == 's':
                    cr.rectangle(i,j,2,1)
                    cr.set_source_rgb(0,255,0)
                if self.tile[(i,j)] == 'w':
                    cr.rectangle(i,j,1,2)
                    cr.set_source_rgb(0,0,255)
                if self.tile[(i,j)] == 'e':
                    cr.rectangle(i,j-1,1,2)
                    cr.set_source_rgb(255,255,0)
            
                cr.fill_preserve()
                cr.set_source_rgb(0,0,0)
                cr.set_line_width(1/20.0)
                cr.stroke()
                
        surface.write_to_png('aztec_%03d.png'%(n))

Order = 127
az = aztec_diamond(0)
for k in range(Order):
    az = az.delete().slide().create()
az.draw()

