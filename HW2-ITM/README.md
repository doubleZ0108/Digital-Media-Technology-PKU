# 第二次作业 - 视频压缩软件使用

<center>姓名：张喆	&emsp;&emsp;&emsp;&emsp;	学号：2101212846	&emsp;&emsp;&emsp;&emsp;	导师：王荣刚教授</center>

[toc]

-----

## 关于第二次作业

### 作业要求

​	使用老师提供的视频压缩软件，编码第一次作业的yuv视频作为测试序列，验证编码和解码过程的正确性，并测试4个不同的码率点画出率失真曲线。

### 系统环境

- **操作系统**：win10
- **处理器**：Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz
- **IDE**：Visual Studio 2017 15.9.39

## 软件环境搭建

​	首先使用Visual Studio 2017打开解决方案`ITM15.0.sln`，再打开提示中进行项目重定向，重定向结果如下：

![image.png](https://upload-images.jianshu.io/upload_images/12014150-4edaf1427b407286.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

​	接着选择`Release`+`Win32`，右键解决方案选择重新生成解决方案，编译后结果如下：

![image.png](https://upload-images.jianshu.io/upload_images/12014150-8d55e17ec9ef9502.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

此时在`bin/`文件夹下生成两个可执行文件`ldecod.exe`和`lencod.exe`，如下：

![image.png](https://upload-images.jianshu.io/upload_images/12014150-759e0eae6acb207f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

通过命令行可以看到，已经可以正确使用ITM软件。

![image.png](https://upload-images.jianshu.io/upload_images/12014150-d3ea877965d6ae3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 软件使用及实验

### 参数配置

​	对于本实验要求的编码解码过程的正确性及不同码率点的失真情况，首先需要更改配置文件`encoder_ra.cfg`和`decoder.cfg`

1. 视频文件读入部分配置参数

> 主要包括输入路径、视频帧率、视频尺寸

```cfg
InputFile              = "D:Digital-Media-Technology-PKUvideo.yuv"			# Input sequence, YUV 4:2:0
InputHeaderLength      = 0    # If the inputfile has a header, state it's length in byte here 
FramesToBeEncoded      = 15  # Number of frames to be coded
SourceWidth            = 320  # Image width  in Pels, must be multiple of 16
SourceHeight           = 240  # Image height in Pels, must be multiple of 16
```

2. 不同码率点配置参数

> 包括第一帧、剩余帧、B帧的量化步长
>
> 量化步长越大，码率越低，失真越大；本实验中简化配置三者相等，分别设置步长：
>
> - 高码率：15
> - 次高码率：25
> - 中码率：35
> - 低码率：45

```cfg
QPFirstFrame          = 15  # Quant. param for first frame (intra) (0-63)
QPRemainingFrame      = 15   # Quant. param for remaining frames (0-63)
QPBPicture            = 15  # Quant. param for B frames (0-63)
```

3. 输出部分配置参数

> 包括解码重建的YUV视频、压缩输出的比特流
>
> 分别设置二者对应四个不同码率，代号分别为`h`, `sh`, `m`, `l`(high, second high, middle, low)

```cfg
ReconFile              = "test_h_rec.yuv"
OutputFile             = "test_h.bit"
```

4. 解码配置参数

> 包括输出的比特流、解码的YUV视频和编码端输出的解码YUV视频

```cfg
test_h.bit                 ........ITM coded bitstream
test_h_dec.yuv             ........Output file, YUV 4:2:0 format
test_h_rec.yuv             ........Ref sequence (for SNR)
```

### 实验步骤

​	对于四个不同的码率分别设置上述参数，然后通过如下第一条指令进行编码，再通过第二条指令进行解码验证，其间记录结果和参数用于后续分析和可视化：

```bash
lencod.exe -f encoder_ra.cfg
ldecod.exe decoder.cfg
```

1. **高码率**

   设置`QPFirstFrame`, `QPRemainingFrame`, `QPBPicture`为15

   1. 编码

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-0f28a23f7b8c3f4b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   2. 编码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-82e87575e21c684e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   3. 解码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-1c776aa727dca955.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. **较高码率**

   设置`QPFirstFrame`, `QPRemainingFrame`, `QPBPicture`为25

   1. 编码

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-ab9d2696ba632599.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   2. 编码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-4b393c58216f3bcf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   3. 解码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-c09055b4646f7c9c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3. **中码率**

   设置`QPFirstFrame`, `QPRemainingFrame`, `QPBPicture`为35

   1. 编码

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-d698c3f2c7d92654.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   2. 编码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-e5b9f88a4ae2a2db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   3. 解码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-451894a20363cf89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4. **低码率**

   设置`QPFirstFrame`, `QPRemainingFrame`, `QPBPicture`为45

   1. 编码

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-93b651b0a94b26b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   2. 编码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-1e7adad521fb12ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

   3. 解码结果

      ![image.png](https://upload-images.jianshu.io/upload_images/12014150-3b38fd06560bea3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

​	经过编解码最终得到的文件列表如下：

![image.png](https://upload-images.jianshu.io/upload_images/12014150-e34a19f4c203575c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 实验结果及分析

​	实验过程中可以直观发现以下结论：

1. 量化步长越大，编码一帧的时间消耗也越短，高码率和低码率相比将近达到20:1
2. 从解码验证输出的SNR可以看到值都为0，意味编码端的预测和解码端的预测是一致的，及编码和解码过程是正确的

​	进一步将所有视频通过YUView观看，可以看到不同码率下的视频状态，主观上在中码率和低码率时有明显的质量降低，同时随着量化步长的提高，码率降低的同时失真逐渐增大。

![image.png](https://upload-images.jianshu.io/upload_images/12014150-4540c07d7ce60d01.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

​	将实验过程中不同码率对应的Bit rate和SNR Y、SNR U、SNR V整理如表所示：

| Bit rate(kbit/s) | SNR Y(dB) | SNR U(dB) | SNR V(dB) |
| ---------------- | --------- | --------- | --------- |
| 3303.15          | 45.88     | 47.03     | 48.01     |
| 1107.28          | 40.50     | 43.03     | 44.43     |
| 346.61           | 35.10     | 38.03     | 40.00     |
| 126.77           | 29.91     | 34.69     | 37.08     |

​	通过Python Matplotlib进行数据绘制，得到如下的率失真曲线：

<img src="https://upload-images.jianshu.io/upload_images/12014150-b89f42e9d547d8da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="Figure_1.png" style="zoom:36%;" />

​	从图中我们可以看到：

1. 随着码率升高，失真变大
2. 相同码率下，失真越小，压缩性能越大
3. 相同失真下，码率越小，压缩性能越大
4. 等间隔采集的四个不同的量化步长，码率的变化率逐步增大，失真的变化率先增大后减小

## 总结

​	本次试验首先编译老师提供的ITM软件，配置不同参数用于验证编码和解码过程的正确性，并测试不同量化步长下的码率和失真情况。通过本次试验对于视频编解码的输入输出有了更加直观的感受，也对课上讲解的重点 —— 率失真曲线有了更加深入的理解，同时本次实验综合了不同课程的知识点，可谓是收获满满，再次感谢王老师～！

## 附录代码

绘制率失真曲线的代码如下所示：

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('data.csv')
x = np.array(data.loc[:, 'Bit rate(kbit/s)'])
y = np.array(data.loc[:, 'SNR Y(dB)'])
u = np.array(data.loc[:, 'SNR U(dB)'])
v = np.array(data.loc[:, 'SNR V(dB)'])

plt.plot(x, y, label='Y')
plt.plot(x, u, label='U')
plt.plot(x, v, label='V')

plt.scatter(x, y, c='black', marker='o')
plt.scatter(x, u, c='blue', marker='s')
plt.scatter(x, v, c='red', marker='^')

plt.title('Rate-Distortion Curce')
plt.xlabel('Bit rate(kbit/s)')
plt.ylabel('PSNR(dB)')

plt.grid(linestyle='-.')
plt.legend(loc='best')

plt.show()
```

