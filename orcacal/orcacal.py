import os
import re
import shutil
import subprocess

from orcacal.AssistFun import update_file_section, delete_and_add_block


def run(ORCA_ins_path, input_file_path, name='input') -> None:
	"""执行 ORCA 计算。

	Args:
		ORCA_ins_path: ORCA 可执行文件的路径。
	"""
	input_file = os.path.join(input_file_path, name + '.inp')
	ORCA_main_path = os.path.join(ORCA_ins_path, 'orca.exe')

	cmd = f'{ORCA_main_path} "{input_file}" > "result.out"'
	temp_name = 'ORCA 计算'

	try:
		print(f'开始 {temp_name}...')
		subprocess.run(cmd, shell=True, check=True)
		print(f'{temp_name} 完成')
	except subprocess.CalledProcessError as e:
		print(f'{temp_name} 失败')
		print(e)
	except Exception as e:
		print(f'发生未知错误:')
		print(e)


def make_molden(ORCA_ins_path, input_file_path, name='input') -> None:
	"""生成 molden 文件并复制重命名。

	Args:
		ORCA_ins_path: ORCA 可执行文件的路径。
		input_file_path: 输入文件的路径。
		name: 输入文件的名称（默认 'input'）。
	"""
	input_file = os.path.join(input_file_path, name)
	ORCA_2mkl_path = os.path.join(ORCA_ins_path, 'orca_2mkl.exe')
	cmd = f'{ORCA_2mkl_path} "{input_file}" -molden'
	temp_name = 'molden 文件生成'

	try:
		print(f'开始 {temp_name}...')
		subprocess.run(cmd, shell=True, check=True)

		old_file = os.path.join(input_file_path, f'{name}.molden.input')
		new_file = os.path.join(input_file_path, f'{name}.molden')

		if os.path.exists(old_file):
			print(f'复制并重命名 {name}.molden.input 为 {name}.molden')
			shutil.copy(old_file, new_file)
		else:
			print(f'{name}.molden.input 文件不存在，无法复制。')

		print(f'{temp_name} 完成')
	except subprocess.CalledProcessError as e:
		print(f'{temp_name} 失败')
		print(e)
	except Exception as e:
		print(f'发生未知错误')
		print(e)


def set_nprocs(input_file_path, jobs=1):
	"""替换或添加 %pal nprocs 内容。"""
	jobs = os.cpu_count() if jobs == -1 else jobs
	new_pal_line = f'% pal nprocs {jobs} end\n'
	pattern = r'^\s*%?\s*pal\s+nprocs\s+\d+\s+end\s*$'
	update_file_section(input_file_path, pattern, new_pal_line, position='end')


def set_maxcore(input_file_path, maxcore=500):
	"""替换或添加 %maxcore 内容。"""
	new_maxcore_line = f'% maxcore {maxcore}\n'
	pattern = r'^\s*%?\s*maxcore\s+\d+\s*$'
	update_file_section(input_file_path, pattern, new_maxcore_line, position='end')


def set_calfun(input_file_path, calfun='! HF DEF2-SVP'):
	"""替换或添加 %set_calfun 内容。"""
	new_maxcore_line = f'! {calfun}\n'
	pattern = r'^\s*!.*$'
	update_file_section(input_file_path, pattern, new_maxcore_line, position='start')


def set_location(input_file_path, location="* xyz 0 1\nO   0.0000   0.0000   0.0626\nH  -0.7920   0.0000  -0.4973\nH   0.7920   0.0000  -0.4973\n*"):
	"""匹配两个 ** 之间的内容并插入到指定位置。"""
	new_content = f'{location}\n'  # 去除多余空格并添加一个换行符
	pattern = r'\*\s*xyz.*?\*'

	# 删除匹配的块，并插入新内容到文件的第 2 行
	delete_and_add_block(input_file_path, pattern, new_content, position=2)


if __name__ == "__main__":
	pass
