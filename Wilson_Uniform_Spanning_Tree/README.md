# Wilson 的一致生成树算法

Wilson 算法是一个在概率论中（random walk, percolation theory, etc.）非常重要的算法，虽然它的表述比较简单，但是算法正确性的证明却很复杂。

我用的 ```cairo``` 绘制的，效率还不错。还做了一个 gif 动画演示宽度优先搜索。

![maze](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Wilson_Uniform_Spanning_Tree/Wilson_Uniform_Spanning_Tree.png)

```Wislon_Uniform_Spanning_Tree_Animation.py``` 这个脚本会在当且目录下生成若干 ```.png``` 文件，然后用 ```ImageMagick``` 将其合成为 .gif 文件：

``` convert -layers Optimize -delay 10 maze*.png BFS_Path_Finding.gif```

这个脚本写的有点复杂：需要随时判断是否到达了终点，否则就每隔 50 步绘制一次。每次绘制除了需要绘制背景的迷宫之外，还要绘制已经访问过的顶点，这个可以保存在一个字典里面，其中字典的每个元素形如 ```v: w``` 且 ```w --> v```。之所以用一个字典来保存已经访问过的点是为了在到达终点时可以还原出到达的路径来。


![path](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Wilson_Uniform_Spanning_Tree/BFS_Path_Find.gif)
