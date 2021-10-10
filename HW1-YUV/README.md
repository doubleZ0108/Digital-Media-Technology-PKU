# 第一次作业 - YUV文件的存储与观察

<center>姓名：张喆		&emsp;&emsp;&emsp;&emsp;		学号：2101212846		&emsp;&emsp;&emsp;&emsp;		导师：王荣刚教授</center>

[toc]

-----

## 关于第一次作业

### 作业要求

​	将摄像头采集到的数据存成YUV文件，并用yuvviewer观察正确性

- **帧率**：15fps
- **尺寸**：320 * 240
- **色度格式**：4:2:0

### 系统环境

- **操作系统**：macOS Big Sur 11.6
- **IDE**：VSCode 1.60.2
- **Python版本**：v3.7.11(conda)
- **FFmpeg版本**：v4.0
- **OpenCV版本**：v3.4.2

## 视频采集与格式转换

​	首先使用手机(iPhone 11)进行视频采集，拍摄参数如下：

- **分辨率**：1080p
- **帧率**：30fps
- **总时长**：14s
- **视频格式**：.MOV

​	接下来分别使用两种不同的工具进行格式转换。



### FFmpeg

​	首先使用如下命令安装FFmpeg工具：

```bash
brew install ffmpeg
```

<img src="https://upload-images.jianshu.io/upload_images/12014150-5b4156fb4d4a4516.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="image.png" style="zoom:50%;" />

进行格式转换需要用到的参数：

- `-i`：指定输入的视频流
- `-r` / `-rate`：指定视频帧率
- `-s` / `-size`：指定视频分辨率（尺寸）
- `-pix_fmt`：指定视频色度格式

​	这里通过如下指令进行本作业要求的格式转换：

```bash
ffmpeg -i video.MOV -r 15 -s 320x240 -pix_fmt yuv420p video-ffmpeg.yuv
```

​	最终得到生成的`video.yuv`视频文件

### OpenCV

​	再通过OpenCV中的视频编解码器进行yuv格式视频的转换，代码如下：

​	其中`cv2.VideoWriter_fourcc()`为四字符代码编解码器，这里使用该函数将原始视频转换为4:2:0色度的yuv视频

```python
import cv2

# 读取原视频
cap = cv2.VideoCapture("video.MOV")

# 设置输出尺寸和帧率
size = (320, 240)
fps = 15

# 使用VideoWriter_fourcc视频编解码器写出yuv格式视频
videoWriter = cv2.VideoWriter("video-opencv.yuv", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)

# 读如第一帧判断视频读取成功与否
if cap.isOpened():
    ret, frame = cap.read()
else:
    ret = False

while ret:
    # 设置输出帧率和尺寸
    frame = cv2.resize(frame, size)
    videoWriter.write(frame)
    ret, frame = cap.read()

cap.release()
```

## 观察YUV视频结果

​	下载[YUView](https://github.com/IENT/YUView)进行观察

### FFmpeg处理

​	可以发现YUV格式的视频存在很大的问题，从参数上看也不符合要求

<img src="https://upload-images.jianshu.io/upload_images/12014150-cb1f7a7580b42912.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="image.png" style="zoom:50%;" />

​	经过研究发现YUView右侧参数需要手动进行设置，经过参数设置之后，YUV格式视频可以正确显示

<img src="https://upload-images.jianshu.io/upload_images/12014150-138f64a377f03e48.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="image.png" style="zoom:50%;" />

### OpenCV处理

​	同样将OpenCV处理后的yuv视频通过YUView进行播放，同样要设置好视频参数，得到的结果如下：

<img src="https://upload-images.jianshu.io/upload_images/12014150-48583ed7d2e9e6e7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="image.png" style="zoom:50%;" />

​	但从视觉效果来看，OpenCV处理得到的yuv视频感官较差，有较强的交织效果和颗粒效果，猜想可能部分与算法的深入设置和研究有关。

## 总结

​	通过第一次作业，让我对课上讲解的YUV格式有了更加直观的认识，也对视频处理有了入门的了解。本次作业通过FFmpeg和OpenCV两个工具进行视频格式的转换，并且通过YUView软件进行结果的观察。其中在工具选用和实现过程中阅读并实操，在结果观察时对遇到的问题进行分析，与课上内容相呼应，非常好的了解了这部分的知识，感谢王老师～！
