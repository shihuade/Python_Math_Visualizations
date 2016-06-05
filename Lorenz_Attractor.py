#coding = utf-8

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint  
from mpl_toolkits.mplot3d import Axes3D  


# 绘制轨迹的个数
N = 20
# 参数
sigma, beta, rho = 10.0, 8/3.0, 28.0

def derivative((x,y,z),t0):
    """返回点 (x,y,z) 处的切方向"""
    return sigma*(y-x), x*(rho-z)-y, x*y-beta*z

def solution(x_0,t):
    """对初始位置 x_0 和时间数组 t, 返回解在 t 的每个元素处的值
    sicpy.odeint() 函数接受一个函数 f, 一个初始值 x_0 和一个列表 t 为参数, 返回值是 t 对应的解组成的列表.
    f 应当为　dy/dt = f(y,t) 返回解 y 在 t 时刻的导数值.
    """
    return odeint(derivative,x_0,t) 

x_0 = -15 + 30 * np.random.random((N,3)) # 随机生成 N 个点
t = np.linspace(0,4,1001)
x_t = np.array([ solution(z,t) for z in x_0])


# 每个点 z 的轨迹是一条空间曲线 z(t), 对区间[0,4]中的 t 计算 z(t), 把这些点连起来就得到了轨迹.
# >>> x_t.shape
# >>> (20,1000,3)


fig = plt.figure(figsize=(8,8))
ax = fig.gca(projection='3d',xlim=(-25,25), ylim=(-35,35),zlim=(5,55))
ax.view_init(30,0) #(初始视角包含 xy 平面的经度和 z 轴的纬度)
ax.axis('off')

# 接下来把要绘制的轨迹和小球各自放在一个列表中. 首先我们生成轨迹和球的列表, 但是先不给出具体值.
# 这里的 ax.plot() 函数返回的是一个长度为 1 的列表, 所以要用 l,=ax.plot() 的写法.

colors = plt.cm.jet(np.linspace(0,1,N))
lines = []
points = []

for c in colors:
    l, = ax.plot([],[],'-',c=c)
    p, = ax.plot([],[],'o',c=c)
    lines.append(l)
    points.append(p)

def init():
    for line, point in zip(lines,points):
        line.set_data([],[])
        line.set_3d_properties([])

        point.set_data([],[])
        point.set_3d_properties([])
    return lines + points

def animate(i):
    i = (2*i) % x_t.shape[1]  # 调整轨迹运动的速度, 否则太慢了
    for line, point, x_j in zip(lines,points,x_t):
        x,y,z = x_j[:i].T

        line.set_data(x,y)
        line.set_3d_properties(z)

        point.set_data(x[-1:],y[-1:]) 
        point.set_3d_properties(z[-1:])
    ax.view_init(30, 0.3*i)
    fig.canvas.draw() 
    return lines + points 

# 这里要把 x_j 当前的端点画出来, 这个点坐标就是 a,b,c = x_j[i], 因此这里也可以写成
# point.set_data([a],[b]) 
# point.set_3d_properties([c])
# 其中 a,b,c 分别是 x_j[i] 的 3 个坐标. 由于 plot() 接受列表为参数, 因此要加 [].
# 试比较 x[-1] 与 x[-1:] 的区别:
# >>> x =[1,2,3]
# >>> x[-1]
# >>> 3
# >>> x[-1:]
# >>> [3]

anim = FuncAnimation(fig,animate,init_func=init,frames=500,interval=30,blit=True)
plt.show()
#anim.save('Lorenz.mp4')
