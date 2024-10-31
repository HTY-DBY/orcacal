import os
import re
import shutil
import subprocess

from orcacal.AssistFun import delete_and_add_block, update_file_section


def run(ORCA_ins_path, input_file_path, input_name='input', output_name='result') -> None:
	"""执行 ORCA 计算并将输出结果保存到指定文件。

	Args:
		ORCA_ins_path: ORCA 安装目录。
		input_file_path: 输入文件所在的路径。
		input_name: 输入文件的基本名称（不包括扩展名），默认是 'input'。
		output_name: 输出结果文件的基本名称（不包括扩展名），默认是 'result'。
	"""
	input_file = os.path.join(input_file_path, f'{input_name}.inp')
	result_file = os.path.join(input_file_path, f'{output_name}.out')
	ORCA_main_path = os.path.join(ORCA_ins_path, 'orca.exe')

	cmd = f'{ORCA_main_path} {input_file} > {result_file}'
	temp_name = 'ORCA 计算'

	try:
		print(f'开始 {temp_name}...')
		subprocess.run(cmd, shell=True, check=True)
		print(f'{temp_name} 完成')
	except subprocess.CalledProcessError as e:
		print(f'{temp_name} 失败')
		print(e)
	except Exception as e:
		print('发生未知错误:')
		print(e)


def make_molden(ORCA_ins_path, input_file_path, name='input') -> None:
	"""生成 Molden 文件并将其复制并重命名。

	Args:
		ORCA_ins_path: ORCA 安装目录。
		input_file_path: 输入文件所在的路径。
		name: 输入文件的基本名称（不包括扩展名），默认是 'input'。
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
		print('发生未知错误')
		print(e)


def set_nprocs(input_file_path, jobs=1):
	"""替换或添加 %pal nprocs 内容以设置并行计算的处理器数量。

	Args:
		input_file_path: 输入文件的路径。
		jobs: 要设置的处理器数量，默认是 1。如果设置为 -1，将使用可用的 CPU 核心数量。
	"""
	jobs = os.cpu_count() if jobs == -1 else jobs
	new_pal_line = f'% pal nprocs {jobs} end\n'
	pattern = r'^\s*%?\s*pal\s+nprocs\s+\d+\s+end\s*$'
	update_file_section(input_file_path, pattern, new_pal_line, position='end')


def set_maxcore(input_file_path, maxcore=500):
	"""一个核心的最大内存使用量

	Args:
		input_file_path: 输入文件的路径。
		maxcore: 要设置的最大内存大小（单位为 MB），默认是 500。
	"""
	new_maxcore_line = f'% maxcore {maxcore}\n'
	pattern = r'^\s*%?\s*maxcore\s+\d+\s*$'
	update_file_section(input_file_path, pattern, new_maxcore_line, position='end')


def set_calfun(input_file_path, calfun=''):
	"""替换或添加 %set_calfun 内容以设置计算方法。

	Args:
		input_file_path: 输入文件的路径。
		calfun: 要设置的计算方法字符串，默认为 '! HF DEF2-SVP LARGEPRINT'。
	"""
	if not calfun: calfun = '! HF DEF2-SVP LARGEPRINT'
	new_maxcore_line = f'{calfun}\n'
	pattern = r'^\s*!.*$'
	update_file_section(input_file_path, pattern, new_maxcore_line, position='start')


def set_location(input_file_path, location=''):
	"""匹配文件中两个 ** 之间的内容并插入新的位置描述。

	Args:
		input_file_path: 输入文件的路径。
		location: 要分析的物质的原子的位置描述，默认是 H2O 的笛卡尔坐标。
	"""
	if not location: location = f'* xyz 0 1\nO   0.0000   0.0000   0.0626\nH  -0.7920   0.0000  -0.4973\nH   0.7920   0.0000  -0.4973\n*'
	new_content = f'{location}\n'  # 去除多余空格并添加换行符
	pattern = r'\*\s*xyz.*?\*'

	# 删除匹配的块，并插入新内容到文件的末尾
	delete_and_add_block(input_file_path, pattern, new_content, position='end')


if __name__ == "__main__":
	pass
