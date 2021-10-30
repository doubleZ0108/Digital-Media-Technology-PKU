# 第四次作业 - E3调整定理证明

<center>姓名：张喆	&emsp;&emsp;&emsp;&emsp;	学号：2101212846	&emsp;&emsp;&emsp;&emsp;	导师：王荣刚教授</center>

[toc]

-----

## 第四次作业要求

​	证明E3调整定理

## E3调整定理定义

​	E3调整解决的核心痛点是在算数编码时，如果low和high在0.5左右无限接近时，二进制高位始终不一样，无法使用E1或E2调整。

​	当区间在[0.25, 0.75)且不满足E1或E2调整时，将区间扩展到[0, 1)范围，公式如下：
$$
E_3(x) = 2(x - 0.5)
$$
​	且调整后暂不输出，直到遇到E1或E2调整时再补偿输出，补偿输出规则如下：
$$
E_1 \circ (E_3)^n = (E_2)^n \circ E_1 \\
E_2 \circ (E_3)^n = (E_1)^n \circ E_2
$$
​	其中$E_i \circ (E_j)^n$代表n次$E_j$调整后紧接一次$E_i$调整，因此有如下性质：

- n次E3调整后跟一次E1调整，等价于1次E1调整后跟n次E2调整
- n次E3调整后跟一次E2调整，等价于1次E2调整后跟n次E1调整

## E3调整定理证明

### E1和E2调整定理

​	首先我们先明确E1和E2调整定理，以下假设整个区间为[0, 1)，当前编码区间为[a, b)

- **E1调整定理**：当[a, b)区间位于[0, 0.5)时，此时最高位bit都是0，将a和b都左移一位并输出0，此时区间长度增加一倍
  $$
  E_{1}\left(\begin{array}{l}
  a \\
  b
  \end{array}\right)=\left(\begin{array}{l}
  2 a \\
  2 b
  \end{array}\right)
  $$

- **E2调整定理**：当[a, b)区间位于[0.5, 1)时，此时最高位bit都是1，将a和b都左移一位并输出1，此时区间长度同样增加一倍
  $$
  E_{2}\left(\begin{array}{l}
  a \\
  b
  \end{array}\right)=\left(\begin{array}{l}
  2 a - 1\\
  2 b - 1
  \end{array}\right)
  $$

### n次$E_i$调整定理$(E_i)^n$

- **n次E1调整后的$(E_1)^n$**：以区间左端点为例，假设第n-1次E1调整后左端点为$x_{n-1}$，第n次E1调整后左端点为$x_n$，易得$x_n = 2 x_{n-1}$，即$x_n$是以$x_1 = 2a$为首项，$q=2$为公比的等差数列，通过通项公式可得
  $$
  x_n = x_1 \cdot q^{n-1}  = 2a \cdot 2^{n-1} = 2^n a
  $$
  区间内的其他点也有同样的性质，由此，n次E1调整后可表达为
  $$
  (E_{1})^n\left(\begin{array}{l}
  a \\
  b
  \end{array}\right)=\left(\begin{array}{l}
  2^n a \\
  2^n b
  \end{array}\right)
  $$

- **n次E2调整后的$(E_2)^n$**：与E1调整类似，第n-1次调整和第n次调整的关系为$y_n = 2y_{n-1} - 1$，即$y_n - 1 = 2(y_{n-1} - 1)$，因此可以把$(y_n - 1)$看作以$y1 - 1 = 2(a-1)$为首项，$q=2$为公比的等比数列，通项公式为
  $$
  y_n - 1 = 2(a-1) \cdot 2^{n-1} \\
  y_n = 2^n a - 2^n + 1
  $$
  同样的，区间内的其他点也有同样的性质，由此，n次E2调整后可表达为
  $$
  (E_{2})^n\left(\begin{array}{l}
  a \\
  b
  \end{array}\right)=\left(\begin{array}{l}
  2^n a - 2^n + 1\\
  2^n b - 2^n + 1
  \end{array}\right)
  $$

- **n次E3调整后的$(E_3)^n$**：第n-1次调整和第n次调整的关系为$z_n = 2z_{n-1} - \frac{1}{2}$，即$z_n - \frac{1}{2} = 2(z_{n-1} - \frac{1}{2})$，因此可以把$(z_n - \frac{1}{2})$看作以$z_1 - \frac{1}{2} = 2(a - \frac{1}{2})$为首项，$q=2$为公比的等比数列，通项公式为

$$
z_n - \frac{1}{2} = (z_1 - \frac{1}{2}) \cdot q^{n-1} = (2a-1) \cdot q^{n-1} = 2^na - 2^{n-1} \\
z_n = 2^n a - 2^{n-1} + \frac{1}{2}
$$
  	与E1和E2调整定理相同，区间内的其他点也有同样的性质，由此，n次E3调整后可表达为
$$
(E_{3})^n\left(\begin{array}{l}
a \\
b
\end{array}\right)=\left(\begin{array}{l}
2^n a - 2^{n-1} + \frac{1}{2}\\
2^n b - 2^{n-1} + \frac{1}{2}
\end{array}\right)
$$

### $E_1 \circ (E_3)^n = (E_2)^n \circ E_1$证明

​	对于等式左侧：
$$
(E_1 \circ (E_3)^n)\left(\begin{array}{l}
a \\
b
\end{array}\right)= E_1\left(\begin{array}{l}
2^n a - 2^{n-1} + \frac{1}{2} \\
2^n b - 2^{n-1} + \frac{1}{2} 
\end{array}\right) = \left(\begin{array}{l}
2 \cdot (2^n a - 2^{n-1} + \frac{1}{2}) \\
2 \cdot (2^n b- 2^{n-1} + \frac{1}{2})
\end{array}\right) = \left(\begin{array}{l}
2^{n+1}a - 2^n + 1 \\
2^{n+1}b - 2^n + 1
\end{array}\right)
$$
​	对于等式右侧：
$$
((E_2)^n \circ E_1)\left(\begin{array}{l}
a \\
b
\end{array}\right) = (E_2)^n \left(\begin{array}{l}
2a \\
2b
\end{array}\right) = \left(\begin{array}{l}
2^n \cdot 2a - 2^n + 1 \\
2^n \cdot 2b - 2^n + 1
\end{array}\right) = \left(\begin{array}{l}
2^{n+1}a - 2^n + 1 \\
2^{n+1}b - 2^n + 1
\end{array}\right)
$$
​	综上，左侧等于右侧，证毕。

### $E_2 \circ (E_3)^n = (E_1)^n \circ E_2$证明

​	对于等式左侧：
$$
(E_2 \circ (E_3)^n)\left(\begin{array}{l}
a \\
b
\end{array}\right)  = E_2\left(\begin{array}{l}
2^n a - 2^{n-1} + \frac{1}{2} \\
2^n b - 2^{n-1} + \frac{1}{2}
\end{array}\right)  = \left(\begin{array}{l}
2^n \cdot (2^n a - 2^{n-1} + \frac{1}{2}) - 1 \\
2^n \cdot (2^n b - 2^{n-1} + \frac{1}{2}) - 1 
\end{array}\right) = \left(\begin{array}{l}
2^{n+1}a - 2^n \\
2^{n+1}b - 2^n
\end{array}\right)
$$
​	对于等式右侧：
$$
((E_1)^n \circ E_2)\left(\begin{array}{l}
a \\
b
\end{array}\right) = (E_1)^n\left(\begin{array}{l}
2a - 1 \\
2b - 1
\end{array}\right) = \left(\begin{array}{l}
2^n(2a - 1)\\
2^n(2b - 1)
\end{array}\right) = \left(\begin{array}{l}
2^{n+1}a - 2^n \\
2^{n+1}b - 2^n
\end{array}\right)
$$
​	综上，左侧等于右侧，证毕。

## 参考

[Arithmetic Coding revealed](http://www.copro.org/download/ac_en.pdf)

