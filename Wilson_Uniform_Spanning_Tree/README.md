# Wilson 的一致生成树算法

用的 ```cairo``` 绘制的，效率还不错。还做了一个 gif 动画演示宽度优先搜索。

![maze](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Wilson_Uniform_Spanning_Tree/Wilson_Uniform_Spanning_Tree.png)

第二个脚本会在当且目录下生成若干 ```.png``` 文件，然后用 ```ImageMagick``` 将其合成为 .gif 文件：

``` convert -layers Optimize -delay 10 maze*.png BFS_Path_Finding.gif```


![path](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Wilson_Uniform_Spanning_Tree/BFS_Path_Finding.gif)
