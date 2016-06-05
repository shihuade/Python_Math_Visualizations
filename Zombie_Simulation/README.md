# Zombie Outbreak in America!

## About this script

Adapted from [Zulko's code](https://gist.github.com/Zulko/6aa898d22e74aa9dafc3) with some mistakes corrected and the dependency on the ```moviepy``` module removed. But you should have ```ImageMagick``` installed on your computer.

This script generates some .png files in current path (the number of image files depends on how long you want to animate) and then one can use the following command to convert them into a gif file:

```convert -layers Optimize -delay 16 zombie*.png zombie.gif```

Now Let's sit down and see the result!

![](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Zombie_Simulation/zombie.gif)


## 关于这个脚本

- Zulko 的程序很不错，但是他的代码有一个关键的地方是错的，而且 moviepy 这个模块对新手来说用起来可能有困难，所以我没有采用。
- 如果把感染者和僵尸的传播速率 ```dispersion_rates``` 设置的比较高的话（比如1，即所有感染者或者僵尸都 "跑起来"），那么整个国家很快就会被横扫，效果不好看，所以低一点好。
- 在 Zulko 的程序中，直接用僵尸的密度```R```代表 RGB 图像中的 R 分量，这个想法是不错的，但是僵尸的扩撒会把整个地图都染成一坨红色，我还是想保留背景地图，所以自己定义了 ```alpha``` 通道。基本的想法就是用 Gamma 校正，让红色比较明显一些，然后红色高的地方透明度低一些。
- 图片中的黄色表示了感染者的传播情况，一个地方总是首先变成黄色再变成彻底的红色，说明这时这里已经彻底的沦陷了。
