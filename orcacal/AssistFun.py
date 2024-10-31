import os
import re


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


def delete_and_add_block(input_file_path, pattern, new_content, position=None):
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

	if position is None or position >= len(modified_lines):
		# 默认添加到末尾
		modified_lines.extend(new_lines)
	else:
		# 插入到指定位置
		modified_lines[position:position] = new_lines

	# 清理多余的空行
	modified_lines = [line for line in modified_lines if line.strip() != '']

	write_file_lines(input_file, modified_lines)
