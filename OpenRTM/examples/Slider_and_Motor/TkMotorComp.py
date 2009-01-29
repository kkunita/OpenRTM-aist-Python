#!/usr/bin/env python

import sys
sys.path.append(".")

import OpenRTM
import RTC

import tkmotor
import time


mod_spec = ["implementation_id", "TkMotorComp", 
	    "type_name", "TkMotorComp", 
	    "description", "Tk Motor component (velocity control)", 
	    "version", "1.0", 
	    "vendor", "Noriaki Ando and Shinji Kurihara", 
	    "category", "Generic", 
	    "activity_type", "DataFlowComponent", 
	    "max_instance", "10", 
	    "language", "Python", 
	    "lang_type""SCRIPT",
	    ""]


tkm = tkmotor.TkMotor(6, 40)
#thread.start_new_thread(tkm.mainloop, ())

class TkMotorComp(OpenRTM.DataFlowComponentBase):
	def __init__(self, manager):
		OpenRTM.DataFlowComponentBase.__init__(self, manager)
		self._tk_data = RTC.TimedFloatSeq(RTC.Time(0,0), [])
		self._tkIn = OpenRTM.InPort("vel", self._tk_data, OpenRTM.RingBuffer(8))

		self.registerInPort("vel", self._tkIn)
		self._cnt = 0
		self._num = 6
		return


	def onActivated(self, ec_id):
		val = [self._cnt] * self._num
		tkm.set_angle(val)
		time.sleep(0.01)
		self._cnt += 1
		self._v = [0] * 6
		return RTC.RTC_OK


	def onExecute(self, ec_id):
		try:
			indata = self._tkIn.read()
			val = indata.data
			print val
			if len(val) == 6:
				for i in range(6):
					self._v[i] += val[i] / 2
				tkm.set_angle(self._v)
		except:
			print "Exception cought in onExecute()"

		time.sleep(0.01)
		return RTC.RTC_OK


	def onShutdown(self, ec_id):
		tkm.quit()
		return RTC.RTC_OK



def MyModuleInit(manager):
	profile = OpenRTM.Properties(defaults_str=mod_spec)
	manager.registerFactory(profile,
				TkMotorComp,
				OpenRTM.Delete)

	# Create a component
	comp = manager.createComponent("TkMotorComp")

	print "Componet created"


def main():
	# Initialize manager
	mgr = OpenRTM.Manager.init(sys.argv)

	# Set module initialization proceduer
	# This procedure will be invoked in activateManager() function.
	mgr.setModuleInitProc(MyModuleInit)

	# Activate manager and register to naming service
	mgr.activateManager()

	# run the manager in blocking mode
	# runManager(False) is the default
	#mgr.runManager()

	# If you want to run the manager in non-blocking mode, do like this
	mgr.runManager(True)
	tkm.mainloop()

if __name__ == "__main__":
	main()