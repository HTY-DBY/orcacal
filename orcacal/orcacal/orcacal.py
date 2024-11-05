import os
import re
import shutil
import subprocess
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

from orcacal.AssistFun import delete_and_add_block, update_file_section, extract_value_from_lines, return_single_or_list, au_to_Debye, calculate_multiplicity


def generate_xyzLocation(smiles: str, charge: int = None, multiplicity: int = None, randomSeed: int = 42) -> str:
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
	location = f"* xyz {charge} {multiplicity}\n{chr(10).join(atom_coords)}\n*"
	return location


def make_molden(input_file_path, input_name, ORCA_2mkl_path) -> None:
	"""生成 Molden 文件并将其复制并重命名。

	Args:
	"""
	input_file = os.path.join(input_file_path, input_name)
	cmd = f'"{ORCA_2mkl_path}" "{input_file}" -molden'
	temp_name = 'molden 文件生成'

	try:
		print(f'开始 {temp_name}...')
		subprocess.run(cmd, shell=True, check=True)

		old_file = os.path.join(input_file_path, f'{input_name}.molden.input')
		new_file = os.path.join(input_file_path, f'{input_name}.molden')

		if os.path.exists(old_file):
			print(f'复制并重命名 {input_name}.molden.input 为 {input_name}.molden')
			shutil.copy(old_file, new_file)
		else:
			print(f'{input_name}.molden.input 文件不存在，无法复制。')

		print(f'{temp_name} 完成')
	except subprocess.CalledProcessError as e:
		print(f'{temp_name} 失败: {e.cmd} 返回码: {e.returncode}')
		print(f'错误输出: {e.output}')
	except Exception as e:
		print('发生未知错误')
		print(e)


class init():

	def __init__(self, ORCA_ins_path: Path or str, input_file_path: Path or str,
				 input_name: str = 'input', output_name: str = 'output') -> None:
		"""
		Args:
			ORCA_ins_path (Path): ORCA 安装目录。
			input_file_path (Path): 输入文件所在的路径。
			input_name (str): 输入文件的基本名称（不包括扩展名），默认是 'input'。
			output_name (str): 输出结果文件的基本名称（不包括扩展名），默认是 'result'。
		"""

		self.ORCA_ins_path = ORCA_ins_path
		self.input_file_path = input_file_path
		self.input_name = input_name
		self.output_name = output_name
		self.ORCA_main_path = os.path.join(self.ORCA_ins_path, 'orca.exe')
		self.ORCA_2mkl_path = os.path.join(self.ORCA_ins_path, 'orca_2mkl.exe')

		# 检查并创建 input_file_path
		if not os.path.exists(self.input_file_path):
			os.makedirs(self.input_file_path)
		# 检查并创建 {self.input_name}.inp
		input_file = os.path.join(self.input_file_path, f"{self.input_name}.inp")
		if not os.path.exists(input_file):
			with open(input_file, 'w') as f:
				f.write("# Creat by orcacal")
			print(f"初始 input.inp 已创建。")

		# function
		self.get = self.get(self)

	def run(self, make_molden_do=True) -> None:
		"""执行 ORCA 计算，输出结果保存到同目录下的 output.out 中。

		Args:
		"""
		input_file = os.path.join(self.input_file_path, f'{self.input_name}.inp')
		output_file = os.path.join(self.input_file_path, f'{self.output_name}.out')

		cmd = f'"{self.ORCA_main_path}" "{input_file}" > "{output_file}"'
		temp_name = 'ORCA 计算'

		try:
			print(f'开始 {temp_name}...')
			subprocess.run(cmd, shell=True, check=True)
			print(f'{temp_name} 完成')
			if make_molden_do: make_molden(self.input_file_path, self.input_name, self.ORCA_2mkl_path)
		except subprocess.CalledProcessError as e:
			print(f'{temp_name} 失败: {e.cmd} 返回码: {e.returncode}')
			print(f'错误输出: {e.output}')
		except Exception as e:
			print('发生未知错误:')
			print(e)

	def set_location(self, location: str = generate_xyzLocation('C(Cl)(Cl)Cl')) -> None:
		"""匹配文件中两个 ** 之间的内容并插入新的位置描述。

		Args:
			location (str): 要分析的物质的原子的位置描述，默认是 H2O 的笛卡尔坐标。
		"""
		new_content = f'{location}\n'
		pattern = r'\*\s*xyz.*?\*'

		# 删除匹配的块，并插入新内容到文件的末尾
		# print(f'原子位置已更新为:\n{location}\n')
		delete_and_add_block(self.input_file_path, pattern, new_content, position='end')

	def set_nprocs(self, nprocs: int = -1) -> None:
		"""替换或添加 %pal nprocs 内容以设置并行计算的处理器数量。

		Args:
			input_file_path (Path): 输入文件的路径。
			nprocs (int): 要设置的处理器数量，默认是 1。如果设置为 -1，将使用最大可用的 CPU 核心数量。
		"""
		if nprocs == -1: nprocs = os.cpu_count()
		new_pal_line = f'% pal nprocs {nprocs} end\n'
		pattern = r'^\s*%?\s*pal\s+nprocs\s+\d+\s+end\s*$'
		update_file_section(self.input_file_path, pattern, new_pal_line, position='end')

	def set_maxcore(self, maxcore: int = 400) -> None:
		"""设置每个核心的最大内存使用量。

		Args:
			input_file_path (Path): 输入文件的路径。
			maxcore (int): 要设置的最大内存大小（单位为 MB），默认是 500。
		"""
		new_maxcore_line = f'% maxcore {maxcore}\n'
		pattern = r'^\s*%?\s*maxcore\s+\d+\s*$'
		update_file_section(self.input_file_path, pattern, new_maxcore_line, position='end')

	def set_calfun(self, calfun: str = '! HF DEF2-SVP LARGEPRINT') -> None:
		"""替换或添加 %set_calfun 内容以设置计算方法。

		Args:
			input_file_path (Path): 输入文件的路径。
			calfun (str): 要设置的计算方法字符串，默认为 '! HF DEF2-SVP LARGEPRINT'。
		"""

		new_maxcore_line = f'{calfun}\n'
		pattern = r'^\s*!.*$'
		update_file_section(self.input_file_path, pattern, new_maxcore_line, position='start')

	def general_set(self, set_dict):
		"""设置通用参数。
		"""
		if 'nprocs' in set_dict: self.set_nprocs(set_dict['nprocs'])
		if 'maxcore' in set_dict: self.set_maxcore(set_dict['maxcore'])
		if 'calfun' in set_dict: self.set_calfun(set_dict['calfun'])
		if 'location' in set_dict: self.set_location(set_dict['location'])

	class get:
		def __init__(self, outer_instance):
			self.outer = outer_instance  # 通过 self.outer 访问外部类实例的属性

		def homo_Lumo_eV(self) -> list or None:
			"""从指定的输出文件中提取 HOMO 和 LUMO 能量值，单位为 eV。

			Returns:
				list or None: [HOMO, LUMO]，包含 HOMO 和 LUMO 能量值的列表；如果未找到数据，则返回 None。
			[HOMO, LUMO] = get.homo_Lumo_eV()
			"""

			input_file_path = self.outer.input_file_path  # 使用外部类的 input_file_path
			output_name = self.outer.output_name  # 使用外部类的 output_name
			# 读取输出文件内容
			with open(os.path.join(input_file_path, f'{output_name}.out'), 'r') as file:
				text = file.read()

			# 定位 "ORBITAL ENERGIES" 部分并匹配数据
			match = re.search(r'ORBITAL ENERGIES.*?\n((?:\s*\d+\s+\d\.\d{4}\s+[-+]?\d+\.\d{6}\s+[-+]?\d+\.\d+\s*\n)+)', text, re.DOTALL)

			if not match:
				return None

			# 获取匹配的能量数据
			data = match.group(1).strip().split('\n')
			transitions = []
			previous_e_ev = None

			# 逐行解析数据以查找 HOMO 和 LUMO 能量值
			for line in data:
				parts = line.split()
				occ = float(parts[1])  # 提取占据数
				e_ev = float(parts[3])  # 提取能量值

				# 检查 OCC 值是否发生到 0 的突变以获取 HOMO 和 LUMO
				if occ == 0 and previous_e_ev is not None:
					transitions.extend([previous_e_ev, e_ev])  # 保存 HOMO 和 LUMO
					break  # 提取到所需值后退出循环

				previous_e_ev = e_ev  # 保存上一个 e_ev 值供突变时使用

			return transitions if transitions else None

		def single_point_energy_Debye(self) -> float or list:
			"""提取单点能量值。

			Args:
				input_file_path (Path): 输入文件的路径。

			Returns:
				[ 3 方向总偶极矩，x，y，z ]
				list: 提取的单点能量值或值的列表。
			"""
			input_file_path = self.outer.input_file_path
			result = extract_value_from_lines(input_file_path, "FINAL SINGLE POINT ENERGY", output_name=self.outer.output_name)
			return return_single_or_list(result)

		def dipolemoment_Debye(self) -> float or list:
			"""提取并转换偶极矩值。

			Args:
				input_file_path (Path): 输入文件的路径。

			Returns:
				float or list: 包含偶极矩值的列表或单个值，[ 3 方向总偶极矩，x，y，z ]。
			"""
			input_file_path = self.outer.input_file_path
			result_3 = extract_value_from_lines(input_file_path, "Total Dipole Moment", output_name=self.outer.output_name)  # 提取分偶极矩，x,y,z
			result_3_debye = au_to_Debye(result_3)  # 将总偶极矩转换为原子单位
			result = extract_value_from_lines(input_file_path, "Magnitude (Debye)", output_name=self.outer.output_name)  # 提取总偶极矩

			# 如果 result_3_debye 是列表，直接拆开并与 result 合并
			# [ 3 方向总偶极矩，x，y，z ]
			result_ALL = result + result_3_debye if isinstance(result_3_debye, list) else result + [result_3_debye]

			return return_single_or_list(result_ALL)


if __name__ == "__main__":
	pass
