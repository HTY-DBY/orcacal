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