import os

import orcacal
from Test.Goble.GSet import GSet_init

GSet = GSet_init()

input_file_path = os.path.join(GSet.ORCA_cal_test_structure, os.path.splitext(os.path.basename(__file__))[0])

atom_coords = orcacal.generate_xyzLocation("O")

orcacal.set_location(input_file_path, location=atom_coords)

orcacal.run(ORCA_ins_path=GSet.ORCA_ins_path, input_file_path=input_file_path)
orcacal.make_molden(ORCA_ins_path=GSet.ORCA_ins_path, input_file_path=input_file_path)

dipolemoment_Debye = orcacal.get.dipolemoment_Debye(input_file_path)
print(dipolemoment_Debye)
single_point_energy_Debye = orcacal.get.single_point_energy_Debye(input_file_path)
print(single_point_energy_Debye)
homo_Lumo_eV = orcacal.get.homo_Lumo_eV(input_file_path)
print(homo_Lumo_eV)
