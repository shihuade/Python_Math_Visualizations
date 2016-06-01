# 将图像转换为铅笔画风格的 Python 实现

This program is a python implementation of the algorithm depicted in the paper [Combining Sketch and Tone for Pencil Drawing Production](http://www.cse.cuhk.edu.hk/~leojia/projects/pencilsketch/pencil_drawing.htm) by CeWu Lu, etc. It transforms a natural image into an artist-drawn style image. It's a single python file (along with a textute image which you can substitute it for your own taste).

## Some technica details

The main steps are all contained in the paper but with some technical minors omitted. To get nice results one has to add a "mean filter smoothing" and a "gamma correction". For example the picture below was smoothed by ```mean_filter(img,5)``` before computing its stroke image and added a gamma correction of factor ```3``` after the stroke computation.

The choice of the edge detection approach is not important.

## 一些技术细节

我在实现这个程序的时候，曾经一直为无法达到作者论文中的效果而不解，甚至怀疑作者是不是隐藏了什么独门技巧没有在论文里写出来。现在经过研究终于达到了理想的效果，上传到 github，希望对大家有所帮助。

这里介绍一下怎样调整参数来实现满意的效果。我们以作者项目主页上的[一副图片](http://www.cse.cuhk.edu.hk/~leojia/projects/pencilsketch/pencil_sketch_images/3--38.htm)为例：

![man.jpg](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Pencil_Draw/man.jpg)

1. 首先选择一副合适的纹理图片，比如这里提供的 ```texture.jpg```。不要选择太稀疏或者有很多小的空白的图片，致密一些的较好。
2. 对输入的图像进行一次均值平滑。注意到背景的天空颜色是渐变的，如果不平滑处理掉的话，这一部分就会有铅笔的笔触显现，而实际上这里应该是画纸的空白。此外图中人手臂上的汗毛也会显得很粗很直，比较难看，所以我们有一个 ```median_filter(I, 5)``` 的代码。
3. 对得到的 ``` stroke``` 图像进行一次 gamma 校正，这幅照片采用的是因子 3。这一步的作用是为了增加图像的线条感。
4. 选择合适的 omega 权重系数。论文给了三组经验系数，我们用 [76, 22, 2] 这一组，得到的结果色调比较浅。

最后得到的结果如下：

![man_result.jpg](https://github.com/wyfly87/Python_Math_Visualizations/blob/master/Pencil_Draw/man_gray.jpg)

是不是比作者的效果还要好一点呢？这应该是选择的纹理图片不同导致的。

还有一些要注意的地方：

- 作者说笔画的长度定义为图片长或者宽的 1/30，这个不要教条的照办，具体图片具体对待。一般来说 11 以内就足够了，涉及到人物的肖像细节的时候更不能设置的太长。
- 处理女孩子的照片的时候，如果有浓密的长发，就要注意权重系数的选择：默认的 ```[76,22,2]``` 会把乌黑的头发变白一部分，而作者给的另外两组 ```[52,37,11]``` 和 ```[42,29,29]``` 色调太黑，所以这时候就要自己灵活设置，用 ```[60,35,5]``` 就不错。 

