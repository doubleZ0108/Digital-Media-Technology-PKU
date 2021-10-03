# 第三次作业 - 整像素运动估计模块分析

<center>姓名：张喆	&emsp;&emsp;&emsp;&emsp;	学号：2101212846	&emsp;&emsp;&emsp;&emsp;	导师：王荣刚教授</center>

[toc]

-----

## 第三次作业要求

​	二选一：

- [x] 找出ITM软件中的整像素运动估计模块代码，并对搜索过程做简要分析
- [ ] 分析OpenCV中的全局运动估计代码，描述其过程

​	本次试验选择第一个任务进行模块分析。

## 背景知识

​	ITM软件中所用到的整像素运动估计算法为`UMHexagonS`，因此本次实验首先对该算法进行调研。

### HMHS算法概述

​	UMHS算法全称是“非对称十字型多层次六边形格点搜索算法”（Unsymmetrieal-CrossMulti-HexagonSearch），被用于H.264中作为快速运动估计算法。该方法有着较大的搜索范围，避免了陷入局部最优解的问题，同时相较于之前H.264的搜索算法精简了搜索点的数量，大大的提高了效率（90%）。该方法适用于各种不同纹理特征和运动剧烈程度的图像帧序列。

​	该算法主要分为四个核心步骤：

1. 起始搜索点预测
2. 非对称的十字交叉搜索（不甚满意区块搜索）
3. 六边形反复搜索（满意区块搜索）
4. 小菱形搜索（很满意区块搜索）

​	其算法流程图大致如下所示：

<img src="https://upload-images.jianshu.io/upload_images/12014150-58317c4b4be3cf30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="image.png" style="zoom:50%;" />

​	接下来将依次简单介绍各步骤。

### 步骤一：起始搜索点预测

​	主要有五种预测方法进行起始搜索点估计：

1. **中值预测**

   利用空间相关性，通过已求出的相邻块的运动矢量求取中间值得到该块的运动矢量初始估计。

2. **原点预测**

   预测初始运动矢量为0，即当前块的位置

   <img src="https://images0.cnblogs.com/i/421096/201406/142242073112923.jpg" alt="img" style="zoom:50%;" />

3. **上层预测**

   运动估计中分块模式有7种

   <img src="https://images0.cnblogs.com/i/421096/201406/142256003119341.jpg" alt="img" style="zoom:50%;" />

   将已求出当前块位置的上一级模式的运动矢量作为当前模式的运动矢量预测值（算法采用从模式1<16\*16>到模式7<4\*4>的分级搜索策略）

   <img src="https://images0.cnblogs.com/i/421096/201406/142333140306188.jpg" alt="img" style="zoom:50%;" />

4. **对应块预测**

   选取前一帧对应位置的运动矢量作为当前块运动矢量的预测值

   <img src="https://images0.cnblogs.com/i/421096/201406/151417225777684.jpg" alt="img" style="zoom:50%;" />

5. **相邻参考帧预测**

   利用时间相关性，将之前的参考帧运动矢量按时间进行缩放

   <img src="https://images0.cnblogs.com/i/421096/201406/151419416558874.jpg" alt="img" style="zoom: 50%;" />

​		往往最后还要进行一次**菱形搜索**，及在周围的小菱形位置中选择最优的运动矢量

<img src="https://images0.cnblogs.com/i/421096/201406/151436277954122.jpg" alt="img" style="zoom:50%;" />

### 步骤二：不甚满意区块搜索

​	在该阶段主要分为三步以决定跳转到接下来的哪个步骤：

1. 以上一步预测的起始搜索点为中心，用非对称十字型搜索(Unsymmetrical-cross search)方法进行寻找，获取当前最佳点，判断该点属于满意或者很满意区，以决定跳转到步骤三、步骤四或继续搜索

   > 先后对x轴和y轴进行搜索，y轴的搜索范围是x轴的一半（一般视频中镜头的纵向移动距离会小一些，横向移动会比较长），隔点进行搜索

   <img src="https://images0.cnblogs.com/i/421096/201406/151540599838531.jpg" alt="img" style="zoom:50%;" />

2. 如果不满意，则以当前最佳点为中心，在5*5的区域中进行全搜索，这里采用的是螺旋搜索(Spiral search)，获取当前最佳点，同样判断是否跳转到之后的步骤

   <img src="https://images0.cnblogs.com/i/421096/201406/152255222175756.jpg" alt="img" style="zoom:50%;" />

3. 如果还是不满意，则用不规则六边形搜索(Uneven multi-Hexagon-grid search)，直至搜索到能复合进入步骤三或步骤四阈值的点为止

   > 以当前位置为圆心，一圈一圈往外搜索，如果在某个圈里找到更加位置，则停止搜索
   
   <img src="https://images0.cnblogs.com/i/421096/201406/152312271247204.jpg" alt="img" style="zoom:50%;" />

### 步骤三：满意区块搜索

​	以当前最佳点为中心进行六边形反复搜索(Extended Hexagon-based search)，直到预测出的最佳点为六边形的中心

> 以当前最佳位置为圆心，反复进行六边形搜索，如若找到更佳位置则更新圆心重新进行六边形搜索

<img src="https://images0.cnblogs.com/i/421096/201406/152336506707192.jpg" alt="img" style="zoom:50%;" />

### 步骤四：很满意区块搜索

​	以当前最佳点为中心进行小菱形搜索(small search pattern)，直到预测出的最佳点为菱形中心

> 与步骤三思路类似，区别在于将六边形替换为菱形

<img src="https://images0.cnblogs.com/i/421096/201406/152358311242089.jpg" alt="img" style="zoom:50%;" />

## 模块分析

​	了解了HMHS算法之后，在ITM项目中进行代码分析。

​	在工程项目中全局搜索`Motion Estimation`，定位到`lecond/inc/fast_me.h`和`lecond/src/fast_me.c`文件中。

<img src="https://upload-images.jianshu.io/upload_images/12014150-a855adcb5e94038f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240" alt="image.png" style="zoom:50%;" />

### 头文件宏函数

​	在头文件中核心模块主要有两个宏函数：

1. `EARLY_TERMINATION`：用于实现第二节讲到的流程图和流程中如果该点已经满意则直接跳转到第二阶段，如果非常满意则跳转到第三阶段。其中满意度是通过SAD(sum of absolute difference)计算得到的。

   ```c
   /* 用于实现第二节讲到的流程图和流程中如果该点已经满意则直接跳转到第二阶段，如果非常满意则跳转到第三阶段。
   			其中满意度是通过SAD(sum of absolute difference)计算得到的。*/
   #define EARLY_TERMINATION  if(ref>0)  \
   	{                                                                    \
   	if ((min_mcost-pred_SAD_ref)<pred_SAD_ref*betaThird)             \
   	goto third_step;                                             \
   	else if((min_mcost-pred_SAD_ref)<pred_SAD_ref*betaSec)           \
   	goto sec_step;                                               \
   	}                                                                    \
   	else if(blocktype>1)                                                 \
   	{                                                                    \
   	if ((min_mcost-pred_SAD_uplayer)<pred_SAD_uplayer*betaThird)     \
   		{                                                                \
   		goto third_step;                                             \
   		}                                                                \
   		else if((min_mcost-pred_SAD_uplayer)<pred_SAD_uplayer*betaSec)   \
   		goto sec_step;                                               \
   	}                                                                    \
   	else                                                                 \
   	{                                                                    \
   	if ((min_mcost-pred_SAD_space)<pred_SAD_space*betaThird)         \
   		{                                                                \
   		goto third_step;                                             \
   		}                                                                \
   		else if((min_mcost-pred_SAD_space)<pred_SAD_space*betaSec)       \
   		goto sec_step;	                                             \
   	}
   ```

2. `SEARCH_ONE_PIXEL`：对于某个在搜索范围内的像素作为预测中心时计算其代价，如果此代价更小则更新最小代价

   ```c
   /* 对于某个在搜索范围内的像素计算其代价，如果此代价更小则更新最小代价 */
   #define SEARCH_ONE_PIXEL  if(abs(cand_x - center_x) <=search_range && abs(cand_y - center_y)<= search_range) \
   		{ \
   		if(!McostState[cand_y-center_y+search_range][cand_x-center_x+search_range])	\
   		{ \
   		mcost = MV_COST (lambda_factor, mvshift, cand_x, cand_y, pred_x, pred_y); \
   		if (ref != -1) { \
   		mcost += REF_COST(lambda_factor, ref);\
   		}\
   		mcost = PartCalMad(ref_pic, orig_pic, get_ref_line,blocksize_y,blocksize_x,blocksize_x4,mcost,min_mcost,cand_x,cand_y); \
   		McostState[cand_y-center_y+search_range][cand_x-center_x+search_range] = mcost; \
   		if (mcost < min_mcost) \
   		{ \
   		best_x = cand_x; \
   		best_y = cand_y; \
   		min_mcost = mcost; \
   		} \
   		} \
   		}
   ```

### 核心算法模块

​	具体运动估计搜索过程通过阅读代码块的注释进一步将核心部分定位到`FastIntegerPelBlockMotionSearch`函数中。

#### 步骤一：起始搜索点预测

​	在初始化所需变量后首先进行起始搜索点的预测，如第二节所述，共采用五种方法，检测顺序依次为中值预测、原点预测、上层块预测、对应块预测、相邻参考帧预测。

1. 中值检测

   ```c
   // 中值预测
   	cand_x = center_x;
   	cand_y = center_y;
   	mcost = MV_COST(lambda_factor, mvshift, cand_x, cand_y, pred_x, pred_y);
   	if (ref != -1) {
   		mcost += REF_COST(lambda_factor, ref);
   	}
   
   	// 计算满意度SAD
   	mcost = PartCalMad(ref_pic, orig_pic, get_ref_line, blocksize_y, blocksize_x, blocksize_x4, mcost, min_mcost, cand_x, cand_y);
   	McostState[search_range][search_range] = mcost;
   	if (mcost < min_mcost)
   	{
   		min_mcost = mcost;
   		best_x = cand_x;
   		best_y = cand_y;
   	}
   
   	iXMinNow = best_x;
   	iYMinNow = best_y;
   	for (m = 0; m < 4; m++)		// 小菱形检测
   	{
   		cand_x = iXMinNow + Diamond_x[m];
   		cand_y = iYMinNow + Diamond_y[m];
   		SEARCH_ONE_PIXEL
   	}
   ```

2. 原点检测

   ```c
   // 原点检测
   	if (center_x != pic_pix_x || center_y != pic_pix_y)
   	{
   		cand_x = pic_pix_x;
   		cand_y = pic_pix_y;
   		SEARCH_ONE_PIXEL
   
   			iXMinNow = best_x;
   		iYMinNow = best_y;
   		for (m = 0; m < 4; m++)
   		{
   			cand_x = iXMinNow + Diamond_x[m];
   			cand_y = iYMinNow + Diamond_y[m];
   			SEARCH_ONE_PIXEL
   		}
   	}
   ```

3. 上层块预测

   ```c
   // 上层块预测
   	if (blocktype>1)
   	{
   		cand_x = pic_pix_x + (pred_MV_uplayer[0] / 4);
   		cand_y = pic_pix_y + (pred_MV_uplayer[1] / 4);
   		SEARCH_ONE_PIXEL
   		if ((min_mcost - pred_SAD_uplayer)<pred_SAD_uplayer*betaThird)
   			goto third_step;
   		else if ((min_mcost - pred_SAD_uplayer)<pred_SAD_uplayer*betaSec)
   			goto sec_step;
   	}
   ```

4. 对应块预测

   ```c
   	//coordinate position prediction
   	// 对应块预测
   	if ((img->number > 1 + ref && ref != -1) || (ref == -1 && Bframe_ctr > 1))
   	{
   		cand_x = pic_pix_x + pred_MV_time[0] / 4;
   		cand_y = pic_pix_y + pred_MV_time[1] / 4;
   		SEARCH_ONE_PIXEL
   	}
   ```

5. 相邻参考帧预测

   ```c
   	//prediciton using mV of last ref moiton vector
   	// 相邻参考帧预测
   	if ((ref > 0) || (img->type == B_IMG && ref == 0))
   	{
   		cand_x = pic_pix_x + pred_MV_ref[0] / 4;
   		cand_y = pic_pix_y + pred_MV_ref[1] / 4;
   		SEARCH_ONE_PIXEL
   	}
   	//strengthen local search
   	iXMinNow = best_x;
   	iYMinNow = best_y;
   	for (m = 0; m < 4; m++)
   	{
   		cand_x = iXMinNow + Diamond_x[m];
   		cand_y = iYMinNow + Diamond_y[m];
   		SEARCH_ONE_PIXEL
   	}
   ```

​	经过五步的初始点寻找后进行`EARLY_TEMINATION`，如果比较满意则跳转到步骤三，如果非常满意则跳转到步骤四，否则继续执行步骤二。

#### 步骤二：不甚满意区块搜索

​	代码中对应`first_step`(*Unsymmetrical-cross search* )，如第二节所述，首先进行非对称十字型搜索，再进行5*5区域全搜索。

1. 非对称十字型搜索

   ```c
   // 非对称十字型搜索
   	for (i = 1; i <= search_range / 2; i++)
   	{
   		search_step = 2 * i - 1;
   		cand_x = iXMinNow + search_step;
   		cand_y = iYMinNow;
   		SEARCH_ONE_PIXEL
   			cand_x = iXMinNow - search_step;
   		cand_y = iYMinNow;
   		SEARCH_ONE_PIXEL
   	}
   	// y轴的搜索范围是x轴的一般
   	for (i = 1; i <= search_range / 4; i++)
   	{
   		search_step = 2 * i - 1;
   		cand_x = iXMinNow;
   		cand_y = iYMinNow + search_step;
   		SEARCH_ONE_PIXEL
   			cand_x = iXMinNow;
   		cand_y = iYMinNow - search_step;
   		SEARCH_ONE_PIXEL
   	}
   ```

2. 5*5区域全搜索

   ```c
   // Uneven Multi-Hexagon-grid Search	
   	// 5*5区域全搜索
   	for (pos = 1; pos < 25; pos++)
   	{
   		cand_x = iXMinNow + spiral_search_x[pos];
   		cand_y = iYMinNow + spiral_search_y[pos];
   		SEARCH_ONE_PIXEL
   	}
   ```

​	同样在此之后进行满意度的判断，决定是否直接跳到最后阶段。

#### 步骤三：满意区块搜索

​	代码中对应`second_step`(*Extended Hexagon-based Search*)

```c
// 六边形反复搜索
	for (i = 0; i < search_range; i++)
	{
		iAbort = 1;
		for (m = 0; m < 6; m++)
		{
			cand_x = iXMinNow + Hexagon_x[m];
			cand_y = iYMinNow + Hexagon_y[m];
			SEARCH_ONE_PIXEL1(0)
		}
		if (iAbort)
			break;
		iXMinNow = best_x;
		iYMinNow = best_y;
	}
```

#### 步骤四：很满意区块搜索

​	代码中对应`third_step`(*the third step with a small search pattern*)

```c
// 小菱形搜索
	for (i = 0; i < search_range; i++)
	{
		iSADLayer = 65536;
		iAbort = 1;
		for (m = 0; m < 4; m++)
		{
			cand_x = iXMinNow + Diamond_x[m];
			cand_y = iYMinNow + Diamond_y[m];
			SEARCH_ONE_PIXEL1(0)
		}
		if (iAbort)
			break;
		iXMinNow = best_x;
		iYMinNow = best_y;
	}
```

## 总结

​	通过本次实验，让我对这两次课上和第二次作业所用到的ITM软件以及视频编码中的技巧有了更加具体也更加直观的感受，作为第一次阅读大型项目源码的实践，在开始时遇到了很大的障碍，不知道该从何开始，经过师兄的点拨，先从背景知识入手，了解HMHS算法的流程步骤以及各阶段的核心方法，再定位到源码中进行对应。而对于课上讲到的运动估计模块也有了更加深入的了解，除了课上讲过的基础算法之外，在真正工程上的编解码器往往有着比较复杂的算法和多种方法的组合方案，也让我对之后课程将要介绍的其他优化方法有了更高的期待。最后感谢王老师一如既往课上的认真付出以及课后的思考～！

## 参考

- [UMHexagonS搜索过程](https://www.cnblogs.com/TaigaCon/p/3788984.html)
- [UMHexagonS算法代码](http://blog.sina.com.cn/s/blog_9b74cfb701018upj.html)
- [UMHexagonS算法优化](https://blog.csdn.net/wh8_2011/article/details/73649717)

