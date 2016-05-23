#coding = utf-8

# An implementation of the Domino Shuffling Algorithm on Aztec Diamond Graphs.

# This script uses the Matplotlib module to make animations of the algorithm.
# Matplotlib gives very nice outputs but it got very slow for large n.
# I suggest using the Cairo version instead when n is greater than 100.

import random
import matplotlib.pyplot as plt
import matplotlib.patches as mps

class Aztec_Diamond:

    def __init__(self,n):
        """
        Use a dict to record a tiling of the graph.
        The keys of the dict are the "coordinates" of the unit squares. 
        Each square is specified by its left bottom corner (i,j).
        The j-th row (j from y=-n to y=n-1) contains min(n+1+j,n-j) unit squares.
        Use "n", "s", "w", "e", "x" to represent the states of the squares.
        """
        
        self.order = n
        self.tile = dict()
        for j in range(-n,n):
            k = min(n+1+j,n-j)
            for i in range(-k,k):
                self.tile[(i,j)] = 'x'
                
    def delete(self):
        """
        Delete all bad blocks in a tiling.
        A bad block is a pair of dominoes that lie in a 2x2 square
        and move towards each other under the shuffling.
        To find all the bad blocks one must start the searching from the boundary.
        """
        n = self.order
        for j in range(-n,n):
            k = min(n+1+j,n-j)
            for i in range(-k,k):
                try:
                    if ((self.tile[(i,j)]=='n'
                         and self.tile[(i+1,j)]=='n'
                         and self.tile[(i,j+1)]=='s'
                         and self.tile[(i+1,j+1)]=='s')
                        or
                        (self.tile[(i,j)]=='e'
                         and self.tile[(i,j+1)]=='e'
                         and self.tile[(i+1,j)]=='w'
                         and self.tile[(i+1,j+1)]=='w')):
                        
                        self.tile[(i,j)]='x'
                        self.tile[(i+1,j)]='x'
                        self.tile[(i,j+1)]='x'
                        self.tile[(i+1,j+1)]='x'
                except:
                    pass
        return self

    def slide(self):
        n = self.order
        new_board = Aztec_Diamond(n+1)
        for (i,j) in self.tile.keys():
            if self.tile[(i,j)] == 'n': new_board.tile[(i,j+1)] = 'n'
            if self.tile[(i,j)] == 's': new_board.tile[(i,j-1)] = 's'
            if self.tile[(i,j)] == 'w': new_board.tile[(i-1,j)] = 'w'
            if self.tile[(i,j)] == 'e': new_board.tile[(i+1,j)] = 'e'
        return new_board

    def create(self):
        """
        To fill in the bad blocks one must start the searching from the boundary.
        """
        n = self.order
        for j in range(-n,n):
            k = min(n+1-j,n-j)
            for i in range(-k,k):
                try:
                    if (self.tile[(i,j)] == 'x'
                        and self.tile[(i+1,j)] == 'x'
                        and self.tile[(i,j+1)] == 'x'
                        and self.tile[(i+1,j+1)] == 'x'):

                        if random.random() > 0.5:
                            # Here we fill the bad blocks with a pair of dominoes leaving each other.
                            # Since a bad block in az(n) will be a good block in az(n+1).

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


    def draw(self, fig_num):
        global fig, Order
        n = self.order
        LineWidth = fig.dpi * fig.get_figwidth() / (20.0*(Order+1))
        ax = fig.add_axes([0,0,1,1], aspect=1)
        ax.axis([-Order-1,Order+1,-Order-1,Order+1])
        ax.axis('off')
        for (i,j) in self.tile.keys():
            if (i+j+n) % 2 == 1:
                if self.tile[(i,j)] == 'n':
                    p = mps.Rectangle((i-1,j),2,1,fc='r')
                    p.set_linewidth(LineWidth)
                    p.set_edgecolor('w')
                    ax.add_patch(p)
                if self.tile[(i,j)] == 's':
                    p = mps.Rectangle((i,j),2,1,fc='y')
                    p.set_linewidth(LineWidth)
                    p.set_edgecolor('w')
                    ax.add_patch(p)
                if self.tile[(i,j)] == 'w':
                    p = mps.Rectangle((i,j),1,2,fc='b')
                    p.set_linewidth(LineWidth)
                    p.set_edgecolor('w')
                    ax.add_patch(p)
                if self.tile[(i,j)] == 'e':
                    p = mps.Rectangle((i,j-1),1,2,fc='g')
                    p.set_linewidth(LineWidth)
                    p.set_edgecolor('w')
                    ax.add_patch(p)

        fig.savefig('Aztec_Diamond_Matplotlib_%03d.png'%(fig_num))
        fig.clear()
        return self

fig = plt.figure(figsize=(6,6))
Order = 40
az = Aztec_Diamond(0)

# Use the following line to draw the frames of the animation
#for k in range(Order):
#    az = az.delete().draw(3*k).slide().draw(3*k+1).create().draw(3*k+2)

# To draw a random tiling of az(n) with n fixed, use the following lines instead: 
#for k in range(Order):
#    az = az.delete().slide().create()
#az.draw(Order)

#-----------------------------------------------------------------------------------
# ImageMagick command to make a gif animation:
# convert -delay 12 -layers Optimize -loop 0 Aztec*.png Aztec_Diamond_Matplotlib.gif
#-----------------------------------------------------------------------------------
