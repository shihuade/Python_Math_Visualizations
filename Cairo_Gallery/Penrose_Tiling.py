# coding = utf-8

import numpy as np
import cairo


num_divides = 5
Width, Height = 600, 600

a = (np.sqrt(5)-1) / 2

def subdivide(triangles):
    result = []
    for color, A, B, C in triangles:
        if color == 0:
            P = A + (B - A) * a 
            result += [(0, C, P, B), (1, P, C, A)]
        else:
            Q = B + (A - B) * a 
            R = B + (C - B) * a
            result += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
    return result

triangles = []

for i in range(10):
    B = np.exp(1j*(2*i-1)*np.pi/10)
    C = np.exp(1j*(2*i+1)*np.pi/10)
    if i%2 == 0:
        B, C = C, B
    triangles.append((0,0j,B,C))

for i in range(num_divides):
    triangles = subdivide(triangles)

surface = cairo.SVGSurface("Penrose_Tiling.svg", Width, Height)
cr = cairo.Context(surface)
cr.translate(Width/2., Height/2.)
cr.scale(0.45*Width,0.45*Height)
cr.set_source_rgb(1,1,1)
cr.paint()

color, A, B, C = triangles[0]
cr.set_line_width(abs(B - A) / 20.0)
cr.set_line_join(2)

for color, A, B, C in triangles:
    D = B + C - A
    cr.move_to(A.real, A.imag)
    cr.line_to(B.real, B.imag)
    cr.line_to(D.real, D.imag)
    cr.line_to(C.real, C.imag)   
    cr.close_path()
    if color == 1:
        cr.set_source_rgb(1.0, 0.078, 0.576)
    else:
        cr.set_source_rgb(0, 0.545, 0.545)
    cr.fill_preserve()
    cr.set_source_rgb(0.2, 0.2, 0.2)
    cr.stroke()

surface.show_page()
