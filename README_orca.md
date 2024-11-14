[toc]

# 1. 前言

本指南将结合 Multiwfn 和 python 对 ORCA 的计算进行说明。

## 1.1. ORCA 简介

ORCA 是一款对学术用户免费但不开源的量子化学程序；它主要由 Frank Neese 设计开发，是包含了从头计算、DFT、半经验方法和耦合簇的量子化学程序包。
ORCA 可以处理溶剂化和相对论效应，同时特别着重于开壳层分子的光谱计算；可以进行几何优化计算，以及预测大量的不同理论级别的光谱参数。

## 1.2. Multiwfn 简介

Multiwfn 是开源免费的波函数分析程序，提供许多重要的分析方法，如 ADCH 原子电荷、拉普拉斯键级、范德华势、hole-electron/IFCT/CTS 电子激发分析等。

# 2. 安装

## 2.1. ORCA 的安装

在 ORCA 官网 <https://orcaforum.kofo.mpg.de/app.php/dlext/> 可下载最新的的 ORCA 安装包（需要全局魔法）。
`必须注册账号`后，页面才会有各个版本的下载显示。截至 2024-11-13，已更新至 6.0.1 版本，该版本的具体需要下载的文件和安装方法见后文。由于你肯定会需要用到并行功能，所有我会连同并行方式一并讲解。

在本文中，以 `{orcaIns}` 表示 orca 的安装路径。

### 2.1.1. Windows 下安装

在 ORCA 官网下载 `ORCA 6.0.1, Windows, 64bit, Installer`

![](https://i-blog.csdnimg.cn/direct/549800b332564d958b3f564561326666.png)

解压由 `ORCA 6.0.1, Windows, 64bit, Installer` 下载的 `Orca6.0.1.Win64.zip`，双击 `Orca6.0.1.Win64.exe` 进行安装。

这里务必选择完整安装：

![](https://i-blog.csdnimg.cn/direct/23a67b6b80e94245bc624ddc4eaabfa4.png)

在项目目录中新建 input.inp 文件，令其内容为：

```bash
! HF DEF2-SVP LARGEPRINT

* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

在当前目录下使用终端，运行 `{orcaIns}/orca input.inp > output.out`，未报错且目录下产生大量文件则表示 ORCA 安装成功。

在微软官网下载 <https://www.microsoft.com/en-us/download/details.aspx?id=57467> 下载并安装 Microsoft MPI v10.0 的 `msmpisetup.exe`。

在项目目录中新建 input.inp 文件，令其内容为：

```bash
! HF DEF2-SVP LARGEPRINT
% pal nprocs 2 end
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

在当前目录下使用终端，运行 `{orcaIns}/orca input.inp > output.out`，未报错且目录下产生大量文件则表示 ORCA 并行功能安装成功。

### 2.1.2. Linux 下安装

### 2.1.3. Mac 下安装

作者无 Mac 电脑，无法对此做出详细教程。

## 2.2. Multiwfn 安装

在 Multiwfn 官网 <http://sobereva.com/multiwfn/> 下载

# 3. ORCA 的运行

## 3.1. 通用流程

首先安装 ORCA。在工作目录下编纂一个输入文件，例如：input.inp；确定一个输出文件名称，例如：output.out。

终端中运行命令: `{orcaIns}/orca input.inp > output.out`。

可以填入具体路径，例如 `a/b/c/input.inp`，建议加双引号避免空格错误。例如`"a f/b e/c/input ggg.inp"`，具体写作：
`"{orcaIns}/orca" "a f/b e/c/input ggg.inp" > "ww/yy/f f/output aaa.out"`

如果配置了环境变量，则可以使用: `orca input.inp > output.out`，但这是不推荐的，因为无法调用并行计算功能。

ORCA 运行后至少会在当前目录下产生 output.out 和 output.gbw 两个文件。

## 3.2. 输入文件

输入文件 input.inp 的通用结构如下，关键字不区分大小写，以水分子为例：

```bash
# 控制方法、基组、工作类型，这个需要放在第一行
! HF DEF2-SVP LARGEPRINT

# 后面的模块模块间没有顺序可言，先写哪个都行

# 输入坐标类型，电荷和自旋多重度。笛卡尔坐标的默认单位是埃
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
# 坐标输入区结束

# $new_job # 可选，新建一个任务，以此类推
# .....
```

`#`是 ORCA 中的注释符号，被注释掉后的部分不被程序读取。

`!` 写在开头，描述控制方法、基组、工作类型

`* xyz 0 1`中，xyz 表示笛卡尔坐标系，内坐标的写法不常用，这里不再展开描述。
0 是分子的总电荷，1 是分子的自旋多重度（等于分子总自旋数的两倍再加一）

## 3.3. 控制方法、基组、工作类型

### 3.3.1. 密度泛函查询

<https://www.faccts.de/docs/orca/6.0/manual/contents/structure.html#density-functional-methods>

### 3.3.2. 基组查询

<https://www.faccts.de/docs/orca/6.0/manual/contents/structure.html#basis-sets>

### 3.3.3. RI 近似

RI 近似默认开启，是 ORCA 的一种降低耗时且损失微乎其微的加速方法。 如果不想使用 RI 则需要输入 `! NoRI` 关闭。不建议。

ORCA5 支持如下几种类型的 RI 近似，都可以在关键词行中直接定义：`! RIJ`，`! RIJK`，`! RIJONX`，`! RIJCOSX`

一般用`! RIJCOSX` 即可，优势明显。杂化泛函计算时默认开启的，关掉则需要输入 `!noCOSX` 关闭。

### 3.3.4. `! Freq` 频率计算

### 3.3.5. `! Opt` 几何优化

### 3.3.6. 关闭布居分析

默认情况下，在计算完自洽场后会自动执行 Mulliken 布居分析、Loewdin 布居分析和 Mayer 布居分析。
下面是手动设置是否分析的关键词：

- `! NoMulliken` 关闭 Mulliken 布居分析
- `! NoLoewdin` 关闭 Loewdin 布居分析
- `! NoMayer` 关闭 Loewdin 布居分析
- `! Allpop` 开启所有布居分析
- `! Nopop` 关闭所有布居分析

### 3.3.7. 自洽场方程的计算模式

- `!NormalSCF` 正常自洽场收敛标准
- `!TightSCF` 严格的自洽场收敛标准
- `!VeryTightSCF` 严格的自洽场收敛标准
- `!SlowConv` 预期收敛较慢
- `!LShift` 开启电平转换
- `!SOSCF` 打开二阶近似自洽场
- `!NRSCF` 打开牛顿-拉夫森自洽场
- `!DIIS` 打开 DIIS
- `!Direct` 直接积分模式
- `!Conv` 传统积分模式
- `!RHF` 闭壳层计算
- `!UHF` 非限制性自旋计算
- `!ROHF` 限制性开壳层计算，需要更多输入参数

### 3.3.8. `! LARGEPRINT`

使用 `! LARGEPRINT`，则可通过 Avogadro 对 output.out 进行轨道可视化和数值显示

## 3.4. 可选的常用非方法模块

### 3.4.1. pal nprocs / maxcore 并行计算

`% pal nprocs` 设置并行计算使用的 CPU 核心数；

`%maxcore` 以 MB 为单位，限制每个核心使用内存的大小：

```bash
! HF DEF2-SVP LARGEPRINT
% pal nprocs 2 end
% maxcore 400
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

### 3.4.2. $new_job 新建任务

新建一个任务，并依此类推：

```bash
! HF DEF2-SVP LARGEPRINT
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
$new_job # 新建一个任务，以此类推
! HF DEF2-SVP LARGEPRINT OPT
* xyz 0 1
O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
*
```

### 3.4.3. xyzfile 读取外部的坐标文件

`xyzfile` 用于读取外部的坐标文件（此方法我没有成功到获取正确的输出文件）：

```bash
! HF DEF2-SVP LARGEPRINT # 控制方法、基组、工作类型
* xyzfile 0 1 H2O.xyz # 电荷和自旋多重度
```

文件 `H2O.xyz` 为：

```bash
3

O   0.0000   0.0000   0.0626
H  -0.7920   0.0000  -0.4973
H   0.7920   0.0000  -0.4973
```

### 3.4.4. 常见输出文件类型

- `.out` 保存了主要的计算结果的信息。
- `.xyz` 包含结构优化后的优化结构。如果优化不成功那么就包含最后一帧的结构。可用作以后读取结构使用。
- `.gbw` 波函数文件。类似于高斯的 chk 文件，包含基态的波函数和结构信息分子结构信息等等。
- `input.molden`/`input.molden.input` 可以载入 Multiwfn 进行分析的文件
- `.nto` 波函数文件，包含有关 TDDFT 计算中的 NTO 轨道的信息可用于多组态的初猜轨道。
- `.uno` 包含 UNO 自然轨道的信息（由！UNO 生成）可用于多组态计算的初猜轨道。
- `.hess` 包含 Hessian 矩阵（频率计算）。计算振动分辨光谱时候会需要用到
- `.allxyz` 坐标文件，柔扫所有点优化好的坐标 适合用于之后的批量单点能计算。
- `.mp2nat` 波函数文件，包含双杂化或者 MP2 计算产生的自然轨道信息。可用作多组态的初猜轨道。
- `.loc` 包含定域轨道信息（通过％loc 块生成）
- `.unso` 包含 UNSO 轨道信息（由！UNO 生成）
- `.qro` 包含 QRO 信息（由！UNO 生成）
- `.trj` 结构优化的轨迹。包含用于柔性表面扫描的所有步骤的整个轨迹，包括每个扫描点的中间优化步骤
- `.00n.xyz` 柔性扫描第 n 点坐标
- `.00n.gbw` 柔性扫描第 n 点波函数
- `.relaxscanscf.dat` 数据文件，包含柔性扫描中所有优化结构的 SCF 能量
- `.relaxscanact.dat` 数据文件，包含柔性扫描中所有优化结构的实际（SCF 或后 HF）能量
- `.properties.txt` 包含了计算中一些主要信息的汇总。

## 3.5. 使用 python 运行 ORCA

安装 `orcacal`：

```bash
pip install orcacal  --upgrade
```

假如你需要在 H2O_1 文件夹内进行计算：

```
D:\H2O
│── input.inp
```

python 代码为：

```python
import orcacal

orcaIns = "D:\hty\ins\ORCA_6"  # ORCA 安装目录
input_file_path = 'D:\H2O'  # 项目目录
project = orcacal.init(orcaIns, input_file_path)  # 初始化计算类
project.run()  # 运行
```

orcacal 的更多使用方法详见后文各案例和 <https://github.com/HTY-DBY/orcacal>

# 4. 常用计算

## 4.1. 几何优化 频率计算

## 4.2. 单点能计算

## 4.3. 福井指数计算

## 4.4. 激发态