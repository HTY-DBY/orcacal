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
