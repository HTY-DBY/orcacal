<h1 align="center">
<img src="https://i.postimg.cc/wjY6JGFL/image.png" width="100">
</h1>

# 1. 前言

`orcacal` 是一个用于通过 Python 调用 ORCA 软件进行计算的库。它封装了常用的计算方法，方便用户在化学计算和模拟中使用。该库旨在简化用户与 ORCA 之间的交互，并提供一个直观的接口来进行各种化学计算。

## 1.1. 特性

- 封装 ORCA 常用计算方法，便于调用和使用
- 提供方便的数据获取、处理和化学特性计算
- 简化的 API 设计，易于上手

# 2. 安装

你可以通过以下方式安装 `orcacal`：

`pip`

```bash
pip install orcacal
```

`conda`

```bash
conda install orcacal
```

# 3. 使用示例

## 3.1. 简单运行

```python
import orcacal

# -- A
# ------input.inp

input_file_path = '运行的项目路径 A'
ORCA_ins_path = 'ORCA 的安装路径，请勿输入可执行文件的路径'

# 运行 ORCA 文件 input.inp
orcacal.run(ORCA_ins_path=ORCA_ins_path, input_file_path=input_file_path)

# 输出偶极矩 (Debye)
# 返回 list [总偶极矩, X方向的偶极矩，Y方向的偶极矩，Z方向的偶极矩]
dipolemoment_Debye = orcacal.get.dipolemoment_Debye(input_file_path)
print(dipolemoment_Debye)

# 输出单点能量
single_point_energy_Debye = orcacal.get.single_point_energy_Debye(input_file_path)
print(single_point_energy_Debye)

# 输出 前线轨道 HOMO, LUMO
# 返回 list [HOMO, LUMO]
homo_Lumo_eV = orcacal.get.homo_Lumo_eV(input_file_path)
print(homo_Lumo_eV)

```

## 3.2. 对 input.inp 的内容进行自定义

```python
import orcacal

# -- A
# ------input.inp

input_file_path = '运行的项目路径 A'
ORCA_ins_path = 'ORCA 的安装路径，请勿输入可执行文件的路径'

# 设置计算方法，! HF DEF2-SVP LARGEPRINT，这是 calfun 的默认值
orcacal.set_calfun(input_file_path, calfun=f'! HF DEF2-SVP LARGEPRINT')

# 设置待分析物质的几何空间位置，H2O 的笛卡尔坐标是 location 的默认值
orcacal.set_location(input_file_path, location=f'* xyz 0 1\nO   0.0000   0.0000   0.0626\nH  -0.7920   0.0000  -0.4973\nH   0.7920   0.0000  -0.4973\n*')

# 设置一个核心的最大内存使用量，500MB 是 calfun 的默认值
orcacal.set_maxcore(input_file_path, maxcore=500)

# 设置并行计算的处理器数量，1 是 jobs 的默认值，-1 表示使用全部核心数
orcacal.set_nprocs(input_file_path, jobs='! HF DEF2-SVP LARGEPRINT')

# 运行 ORCA 文件 input.inp
orcacal.run(ORCA_ins_path=ORCA_ins_path, input_file_path=input_file_path)
```

# 4. 在开发的功能

吉布斯能量变换和换算，福井指数

# 5. Star History

[![Star History Chart](https://api.star-history.com/svg?repos=HTY-DBY/orcacal&type=Date)](https://star-history.com/#HTY-DBY/orcacal&Date)
