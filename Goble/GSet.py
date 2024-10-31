import os
from dataclasses import dataclass


@dataclass
class GSet:
	ORCA_ins_path: str = r"D:\hty\ins\ORCA_6"
	ORCA_main_path: str = ""
	ORCA_2mkl_path: str = ""

	ORCA_cal_test: str = os.path.join(os.path.dirname(__file__), '..', 'Test\ORCA_cal')
	ORCA_cal_test_structure: str = os.path.join(ORCA_cal_test, 'ORCA_structure')
	ORCA_cal_test_Cal_byPY: str = os.path.join(ORCA_cal_test, 'ORCA_Cal_byPY')


# def __post_init__(self):
# self.ORCA_main_path = os.path.join(self.ORCA_ins_path, 'orca.exe')
# self.ORCA_2mkl_path = os.path.join(self.ORCA_ins_path, 'orca_2mkl.exe')


def GSet_init():
	return GSet()
