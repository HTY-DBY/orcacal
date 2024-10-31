import os
import shutil
import subprocess
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

from orcacal.AssistFun import delete_and_add_block, update_file_section


def run(ORCA_ins_path: Path, input_file_path: Path, input_name: str = 'input', output_name: str = 'result') -> None:
	"""执行 ORCA 计算，输出结果保存到同目录下的 result.out 中。

	Args:
		ORCA_ins_path (Path): ORCA 安装目录。
		input_file_path (Path): 输入文件所在的路径。
		input_name (str): 输入文件的基本名称（不包括扩展名），默认是 'input'。
		output_name (str): 输出结果文件的基本名称（不包括扩展名），默认是 'result'。
	"""
	input_file = input_file_path / f'{input_name}.inp'
	result_file = input_file_path / f'{output_name}.out'
	ORCA_main_path = ORCA_ins_path / 'orca.exe'

	cmd = f'{ORCA_main_path} {input_file} > {result_file}'
	temp_name = 'ORCA 计算'

	try:
		print(f'开始 {temp_name}...')
		subprocess.run(cmd, shell=True, check=True)
		print(f'{temp_name} 完成')
	except subprocess.CalledProcessError as e:
		print(f'{temp_name} 失败: {e.cmd} 返回码: {e.returncode}')
		print(f'错误输出: {e.output}')
	except Exception as e:
		print('发生未知错误:')
		print(e)


def make_molden(ORCA_ins_path: Path, input_file_path: Path, name: str = 'input') -> None:
	"""生成 Molden 文件并将其复制并重命名。

	Args:
		ORCA_ins_path (Path): ORCA 安装目录。
		input_file_path (Path): 输入文件所在的路径。
		name (str): 输入文件的基本名称（不包括扩展名），默认是 'input'。
	"""
	input_file = input_file_path / name
	ORCA_2mkl_path = ORCA_ins_path / 'orca_2mkl.exe'
	cmd = f'{ORCA_2mkl_path} "{input_file}" -molden'
	temp_name = 'molden 文件生成'

	try:
		print(f'开始 {temp_name}...')
		subprocess.run(cmd, shell=True, check=True)

		old_file = input_file_path / f'{name}.molden.input'
		new_file = input_file_path / f'{name}.molden'

		if old_file.exists():
			print(f'复制并重命名 {name}.molden.input 为 {name}.molden')
			shutil.copy(old_file, new_file)
		else:
			print(f'{name}.molden.input 文件不存在，无法复制。')

		print(f'{temp_name} 完成')
	except subprocess.CalledProcessError as e:
		print(f'{temp_name} 失败: {e.cmd} 返回码: {e.returncode}')
		print(f'错误输出: {e.output}')
	except Exception as e:
		print('发生未知错误')
		print(e)


def set_nprocs(input_file_path: Path, jobs: int = 1) -> None:
	"""替换或添加 %pal nprocs 内容以设置并行计算的处理器数量。

	Args:
		input_file_path (Path): 输入文件的路径。
		jobs (int): 要设置的处理器数量，默认是 1。如果设置为 -1，将使用最大可用的 CPU 核心数量。
	"""
	jobs = os.cpu_count() if jobs == -1 else jobs
	new_pal_line = f'% pal nprocs {jobs} end\n'
	pattern = r'^\s*%?\s*pal\s+nprocs\s+\d+\s+end\s*$'
	update_file_section(input_file_path, pattern, new_pal_line, position='end')


def set_maxcore(input_file_path: Path, maxcore: int = 500) -> None:
	"""设置每个核心的最大内存使用量。

	Args:
		input_file_path (Path): 输入文件的路径。
		maxcore (int): 要设置的最大内存大小（单位为 MB），默认是 500。
	"""
	new_maxcore_line = f'% maxcore {maxcore}\n'
	pattern = r'^\s*%?\s*maxcore\s+\d+\s*$'
	update_file_section(input_file_path, pattern, new_maxcore_line, position='end')


def set_calfun(input_file_path: Path, calfun: str = '! HF DEF2-SVP LARGEPRINT') -> None:
	"""替换或添加 %set_calfun 内容以设置计算方法。

	Args:
		input_file_path (Path): 输入文件的路径。
		calfun (str): 要设置的计算方法字符串，默认为 '! HF DEF2-SVP LARGEPRINT'。
	"""

	new_maxcore_line = f'{calfun}\n'
	pattern = r'^\s*!.*$'
	update_file_section(input_file_path, pattern, new_maxcore_line, position='start')


def set_location(input_file_path: Path, location: str = '* xyz 0 1\nO   0.0000   0.0000   0.0626\nH  -0.7920   0.0000  -0.4973\nH   0.7920   0.0000  -0.4973\n*') -> None:
	"""匹配文件中两个 ** 之间的内容并插入新的位置描述。

	Args:
		input_file_path (Path): 输入文件的路径。
		location (str): 要分析的物质的原子的位置描述，默认是 H2O 的笛卡尔坐标。
	"""
	new_content = f'{location}\n'  # 去除多余空格并添加换行符
	pattern = r'\*\s*xyz.*?\*'

	# 删除匹配的块，并插入新内容到文件的末尾
	delete_and_add_block(input_file_path, pattern, new_content, position='end')
	print(f'原子位置已更新为:\n{location}\n')


def calculate_multiplicity(mol) -> int:
	"""根据分子的未配对电子数量计算自旋多重度。

	Args:
		mol: RDKit 分子对象。

	Returns:
		int: 计算得到的自旋多重度。
	"""
	num_unpaired = 0  # 初始化未配对电子数量
	for atom in mol.GetAtoms():
		# 计算每个原子的未配对电子数量并累加
		num_unpaired += atom.GetNumRadicalElectrons()
	return 1 + num_unpaired  # 自旋多重度为未配对电子数量加 1


def generate_xyz(smiles: str, charge: int = None, multiplicity: int = None, randomSeed: int = 42) -> str:
	"""从 SMILES 创建分子对象并生成带电荷和自旋多重度的笛卡尔坐标系 (xyz)。

	Args:
		smiles (str): 分子的 SMILES 表示。
		charge (int): 分子的电荷，默认为 None。会根据分子计算。
		multiplicity (int): 分子的自旋多重度，默认为 None。会根据分子计算。
		randomSeed (int): 生成 3D 坐标时的随机种子，默认为 42。

	Returns:
		str: 笛卡尔坐标系 (xyz)，包含电荷和自旋多重度信息。
	"""
	# 从 SMILES 创建分子对象，并添加氢原子
	mol = Chem.AddHs(Chem.MolFromSmiles(smiles))

	# 生成 3D 坐标并优化分子几何结构
	AllChem.EmbedMolecule(mol, randomSeed=randomSeed)
	AllChem.UFFOptimizeMolecule(mol)

	# 如果没有提供电荷，则计算分子的电荷
	if charge is None:
		charge = Chem.rdmolops.GetFormalCharge(mol)
	# 如果没有提供自旋多重度，则计算分子的自旋多重度
	if multiplicity is None:
		multiplicity = calculate_multiplicity(mol)

	# 提取原子坐标并格式化为字符串
	atom_coords = [
		f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}"
		for atom in mol.GetAtoms()
		for pos in [mol.GetConformer().GetAtomPosition(atom.GetIdx())]
	]

	# 生成带电荷和多重度的笛卡尔坐标系 (xyz)
	return f"* xyz {charge} {multiplicity}\n{chr(10).join(atom_coords)}\n*"


if __name__ == "__main__":
	pass
