from ScheduleHelper.MOCTC2Y import MOCTC2YHelper
from ScheduleHelper.GeneratePlan import GeneratePlanHelper, SCPlanHelper, CGPlanHelper, CPPlanHelper
from BaseHelper import Logger
import sys
import os


loggerMain = Logger(sys.path[0] + '/Log/Main.log')

if __name__ == '__main__':
	# moctc2y = MOCTC2YHelper(debug=False)
	# moctc2y.work()

	# generatePlan = GeneratePlanHelper(debug=True, host='192.168.1.61')
	# generatePlan.work()

	scPlan = SCPlanHelper(debug=False, host='192.168.1.61')
	cgPlan = CGPlanHelper(debug=False, host='192.168.1.61')
	cpPlan = CPPlanHelper(debug=False, host='192.168.1.61')

	cgPlan.work(td001='2201', td002='000001', td003='0001', planId='22010000010001', planVersion='0001')
