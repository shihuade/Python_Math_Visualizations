# 将图像转换为铅笔画风格的 Python 实现

我在实现这个程序的时候，一直为无法达到作者论文中的效果而苦恼，甚至怀疑作者是不是隐藏了什么独门技巧没有在论文里写出来。现在经过研究终于达到了理想的效果，这里特别写出来，希望对大家有所帮助。

这里介绍一下怎样调整参数来实现满意的效果。我们以作者项目主页上的[一副图片](http://www.cse.cuhk.edu.hk/~leojia/projects/pencilsketch/pencil_sketch_images/3--38.htm)为例：

[!man.jpg](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Pencil_Draw/man.jpg)

1. 首先选择一副合适的纹理图片，比如这里提供的 ```texture.jpg```。不要选择太稀疏或者有很多小的空白的图片，致密一些的较好。
2. 对输入的图像进行一次均值平滑。注意到背景的天空颜色是渐变的，如果不平滑处理掉的话，得到的 stroke 图像上这一部分就会有铅笔的笔触显现，而实际上这里应该是画纸的空白。此外图中人手臂上的汗毛也会显得很粗很直，比较难看，所以我们有一个 ```median_filter(I, 5)``` 的代码。
3. 对得到的 ``` stroke``` 图像进行一次 gamma 校正，这里采用的是因子 2。这一步的作用是为了增加图像的线条感。
4. 选择合适的 omega 权重系数。作者主页给了三组经验系数，我们用 [76, 22, 2] 这一组，得到的结果色调比较浅。

最后得到的结果如下：

[!man_result.jpg](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Pencil_Draw/man_gray.jpg)

是不是比作者的效果还要好一点呢？这应该是选择的纹理图片不同导致的。
