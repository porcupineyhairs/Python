import os
from ScheduleHelper.MOCTC2Y import MOCTC2YHelper
from BaseHelper import Logger

if __name__ == '__main__':
	log_I = Logger(os.path.curdir + '/Log/Main_Info.log', level='info')
	log_E = Logger(os.path.curdir + '/Log/Main_Err.log', level='error')
