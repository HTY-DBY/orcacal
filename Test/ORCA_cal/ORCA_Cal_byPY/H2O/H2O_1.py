import os
import orcacal
from Goble.GSet import GSet_init

GSet = GSet_init()

input_file_path = os.path.join(GSet.ORCA_cal_test_structure, os.path.splitext(os.path.basename(__file__))[0])

# orcacal.set_calfun(input_file_path=input_file_path, calfun='HF DEF2-SVP')
# orcacal.set_location(input_file_path, )
# orcacal.set_nprocs(input_file_path=input_file_path, jobs=os.cpu_count())
# orcacal.set_maxcore(input_file_path=input_file_path, maxcore=1000)
#
# orcacal.run(ORCA_ins_path=GSet.ORCA_ins_path,
# 		   input_file_path=input_file_path,
# 		   # name='input'
# 		   )
# orcacal.make_molden(ORCA_ins_path=GSet.ORCA_ins_path,
# 				   input_file_path=input_file_path,
# 				   # name='input'
# 				   )
