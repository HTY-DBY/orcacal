import os
import re
from pathlib import Path


def read_file_lines(file_path):
	"""读取文件中的所有行。"""
	with open(file_path, 'r') as file:
		return file.readlines()


def write_file_lines(file_path, lines):
	"""将行写入文件。"""
	with open(file_path, 'w') as file:
		file.writelines(lines)


def update_file_section(input_file_path, pattern, new_line, position='end'):
	"""更新文件中指定部分的内容。"""
	input_file = os.path.join(input_file_path, 'input.inp')
	lines = [line for line in read_file_lines(input_file) if not re.match(pattern, line)]

	# 根据指定的位置插入新行
	if position == 'start':
		lines.insert(0, new_line)  # 添加到开头
	elif position == 'end':
		lines.append(new_line)  # 添加到末尾
	else:
		# 将新行插入到指定位置（基于行数）
		try:
			line_position = int(position)
			lines.insert(line_position, new_line)  # 插入到指定行
		except ValueError:
			print("位置参数应为 'start', 'end' 或有效的行号。")
			return

	write_file_lines(input_file, lines)


def delete_and_add_block(input_file_path, pattern, new_content, position='end'):
	"""删除匹配的内容块，并在指定位置添加新内容。"""
	input_file = os.path.join(input_file_path, 'input.inp')
	lines = read_file_lines(input_file)

	# 删除匹配的内容块
	content = ''.join(lines)
	modified_content = re.sub(pattern, '', content, flags=re.DOTALL)

	# 将删除后的内容拆回行列表
	modified_lines = modified_content.splitlines(keepends=True)

	# 插入新内容，确保最后一行以换行符结尾
	new_lines = new_content.rstrip('\n') + '\n' if new_content.strip() else ''
	new_lines = new_lines.splitlines(keepends=True)

	# 检查新内容是否已经存在于文件中
	if any(new_content.strip() in line for line in modified_lines):
		print("新内容已存在，不再插入。")
		return  # 如果已存在，直接返回

	if position == 'end':
		# 默认添加到末尾
		modified_lines.extend(new_lines)
	else:
		# 插入到指定位置
		modified_lines[position:position] = new_lines

	# 清理多余的空行
	modified_lines = [line for line in modified_lines if line.strip() != '']

	write_file_lines(input_file, modified_lines)


def au_to_Debye(au: float or list) -> float or list:
	"""将 原子单位 (a.u.) 转换为 Debye。

	Args:
		au (float or list): 单个浮点数或包含多个值的列表，表示 a.u. 单位的偶极矩值。

	Returns:
		float or list: 如果输入是单个值，返回转换后的浮点数；如果是列表，返回包含转换后值的列表。
	"""
	# 转换因子
	conversion_factor = 2.541797999144788628014310325551

	# 检查输入类型并进行转换
	if isinstance(au, (list, tuple)):
		return [d * conversion_factor for d in au]  # 转换列表中的每个值
	else:
		return au * conversion_factor  # 单个值的情况


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


def extract_value_from_lines(input_file_path: Path, search_str: str, output_name: str) -> list or None:
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
	with open(os.path.join(input_file_path, f'{output_name}.out'), 'r', encoding='utf-8', errors='ignore') as file:
		lines = file.read().splitlines()

	for line in lines:
		if search_str in line:
			# 使用正则表达式查找所有匹配的浮点数
			matches = re.findall(r'-?\d+\.\d+', line)
			if matches:
				# 将匹配的数值转换为浮点数并添加到列表中
				values.extend([float(match) for match in matches])

	return values if values else None


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
