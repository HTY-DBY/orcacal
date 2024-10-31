import os
from dataclasses import dataclass


@dataclass
class GSet:
	ORCA_ins_path: str = r"D:\hty\ins\ORCA_6"
	ORCA_main_path: str = ""
	ORCA_2mkl_path: str = ""

	ORCA_cal_test: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ORCA_cal')
	ORCA_cal_test_structure: str = os.path.join(ORCA_cal_test, 'ORCA_structure')
	ORCA_cal_test_Cal_byPY: str = os.path.join(ORCA_cal_test, 'ORCA_Cal_byPY')


def GSet_init():
	return GSet()


if __name__ == '__main__':
	GSet_init()
