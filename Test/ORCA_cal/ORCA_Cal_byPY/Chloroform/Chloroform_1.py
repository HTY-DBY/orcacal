import os
import orcacal
from Test.Goble.GSet import GSet_init

GSet = GSet_init()

input_file_path = os.path.join(
	GSet.ORCA_cal_test_structure, os.path.splitext(os.path.basename(__file__))[0]
)
# %%
project = orcacal.init(GSet.ORCA_ins_path, input_file_path)  # 初始化计算类

calfun = '! HF DEF2-SVP LARGEPRINT'  # 设置计算方法
maxcore = 400  # 设置每个核心的最大内存使用量
nprocs = -1  # 设置使用的核心数
location = orcacal.generate_xyzLocation('C(Cl)(Cl)C')  # 设置原子位置

project.general_set({
	'calfun': calfun,
	'nprocs': nprocs,
	'maxcore': maxcore,
	'location': location
})

# 一样的方法，只不过分开设置了
# project.set_calfun(calfun)
# project.set_location(location)
# project.set_nprocs(nprocs)
# project.set_maxcore(maxcore)

# project.run()

# %%

# 获取 [HOMO, LUMO]
[HOMO, LUMO] = project.get.homo_Lumo_eV()
print(f'HOMO: {HOMO} eV, LUMO: {LUMO} eV')
# 获取单点能
single_point_energy_Debye = project.get.single_point_energy_Debye()
print(f'single_point_energy_Debye: {single_point_energy_Debye:.5f} Debye')
# 获取偶极矩
dipolemoment_Debye = project.get.dipolemoment_Debye()
print(f'dipolemoment_Debye:\nTotal--{dipolemoment_Debye[0]:.5f}, X-{dipolemoment_Debye[1]:.5f}, Y-{dipolemoment_Debye[2]:.5f}, Z-{dipolemoment_Debye[3]:.5f} Debye')
