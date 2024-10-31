import os
import re
from pathlib import Path


def homo_Lumo_eV(input_file_path: Path, output_name: str = 'result') -> list or None:
	"""从指定的输出文件中提取 HOMO 和 LUMO 能量值，单位为 eV。

	Args:
		input_file_path (Path): 输入文件的路径，包含输出文件的目录。
		output_name (str): 输出文件的名称，不包含扩展名，默认为 'result'。

	Returns:
		list or None: [HOMO, LUMO]，包含 HOMO 和 LUMO 能量值的列表；如果未找到数据，则返回 None。
	"""
	# 读取输出文件内容
	with open(input_file_path / f'{output_name}.out', 'r') as file:
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


def debye_to_a_u(debye: float or list) -> float or list:
	"""将 Debye 单位转换为原子单位 (a.u.)。

	Args:
		debye (float or list): 单个浮点数或包含多个值的列表，表示 Debye 单位的偶极矩值。

	Returns:
		float or list: 如果输入是单个值，返回转换后的浮点数；如果是列表，返回包含转换后值的列表。
	"""
	# 更精确的转换因子
	conversion_factor = 0.393430307

	# 检查输入类型并进行转换
	if isinstance(debye, (list, tuple)):
		return [d * conversion_factor for d in debye]  # 转换列表中的每个值
	else:
		return debye * conversion_factor  # 单个值的情况


def single_point_energy_Debye(input_file_path: Path) -> float or list:
	"""提取单点能量值。

	Args:
		input_file_path (Path): 输入文件的路径。

	Returns:
		float or list: 提取的单点能量值或值的列表。
	"""
	result = extract_value_from_lines(input_file_path, "FINAL SINGLE POINT ENERGY")
	return return_single_or_list(result)


def dipolemoment_Debye(input_file_path: Path) -> float or list:
	"""提取并转换偶极矩值。

	Args:
		input_file_path (Path): 输入文件的路径。

	Returns:
		float or list: 包含偶极矩值的列表或单个值。
	"""
	result_3 = extract_value_from_lines(input_file_path, "Total Dipole Moment")  # 提取总偶极矩
	result_3_debye = debye_to_a_u(result_3)  # 将总偶极矩转换为原子单位
	result = extract_value_from_lines(input_file_path, "Magnitude (Debye)")  # 提取幅值

	# 如果 result_3_debye 是列表，直接拆开并与 result 合并
	result_ALL = result + result_3_debye if isinstance(result_3_debye, list) else result + [result_3_debye]

	return return_single_or_list(result_ALL)


def return_single_or_list(values: list) -> float or list or None:
	"""根据返回的值数量决定返回类型。

	Args:
		values (list): 提取到的数值列表。

	Returns:
		float or list or None: 如果只有一个值，返回该值；如果有多个值，返回值列表；否则返回 None。
	"""
	if values is not None:
		if len(values) == 1:
			return values[0]  # 返回单个值
		return values  # 返回多个值
	return None  # 如果没有找到值


def extract_value_from_lines(input_file_path: Path, search_str: str, output_name: str = 'result') -> list or None:
	"""从给定文本中提取特定字符串的值，并返回所有匹配的浮点数值。

	Args:
		input_file_path (Path): 输入文件的路径，包含输出文件的目录。
		search_str (str): 要搜索的字符串。
		output_name (str): 输出文件的名称，不包含扩展名，默认为 'result'。

	Returns:
		list or None: 所有匹配的浮点数值列表；如果未找到值，则返回 None。
	"""
	values = []

	# 读取输出文件内容
	with open(input_file_path / f'{output_name}.out', 'r', encoding='utf-8', errors='ignore') as file:
		lines = file.read().splitlines()

	for line in lines:
		if search_str in line:
			# 使用正则表达式查找所有匹配的浮点数
			matches = re.findall(r'-?\d+\.\d+', line)
			if matches:
				# 将匹配的数值转换为浮点数并添加到列表中
				values.extend([float(match) for match in matches])

	return values if values else None
