import orcacal

# 经过 ORCA 计算得到 input.gbw 后才能生成，否则报错
# input_file_path = '运行的项目路径 H2O_1'
# ORCA_ins_path = 'ORCA 的安装路径，请勿输入可执行文件的路径'
input_file_path = f"D:\hty\creat\code\github\orcacal\Test\ORCA_cal\ORCA_structure\H2O_1"
ORCA_ins_path = f"D:\hty\ins\ORCA_6"

orcacal.make_molden(ORCA_ins_path, input_file_path, name='input')
