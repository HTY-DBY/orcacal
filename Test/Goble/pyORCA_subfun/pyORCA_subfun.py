import os
import subprocess


class ORCA_Running_pyORCA:
	def __init__(self, ORCA_ins_path):
		"""初始化 ORCAHandler 类"""
		self.ORCA_ins_path = ORCA_ins_path
		self.ORCA_main_path = os.path.join(ORCA_ins_path, 'orca.exe')
		self.ORCA_2mkl_path = os.path.join(ORCA_ins_path, 'orca_2mkl.exe')

	def ORCA_Running_pyORCA(self):
		"""执行 ORCA 计算"""
		cmd = f'{self.ORCA_main_path} input.inp > result.out'
		print('ORCA 计算中...')
		subprocess.run(cmd, shell=True)
		print('ORCA 计算完成')

	def ORCA_2mkl_pyORCA(self):
		"""执行 gbw 转换"""
		cmd = f'{self.ORCA_2mkl_path} input -molden'
		print('gbw 转换中...')
		subprocess.run(cmd, shell=True)
		print('gbw 转换完成')


if __name__ == "__main__":
	pass
