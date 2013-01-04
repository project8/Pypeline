'''
	A class that stores and updates recent data from couch
'''

#Standard libs
from warnings import warn
from datetime import datetime, timedelta
import time

#3rd party libs
from couchdb import Server as CouchServer
import numpy as np
from scipy import optimize
import threading

class CommandMonitor:
	'''
		Class that monitors recent commands from Couchdb
	'''
	def __init__(self, couch_url="http://127.0.0.1:5984"):
		'''
			Connects to data server and looks for logged data.
			Inputs:
			<couch_url> (string) URL of CouchDB server
		'''
		print "connecting to database"
		self._server = CouchServer(couch_url)
		if (self._server.__contains__('dripline_cmd')):
			self._cmd = self._server['dripline_cmd']
		else:
			raise UserWarning('The dripline command data database was not found!')
		#some defaults and internal variables
		self.continuous_logging=False
		self.do_on_update={}
		self.do_on_update_mutex=threading.Lock()
		self.data_mutex=threading.Lock()
		#by default, load data from the last three hours
		self.last_seq=self._cmd.info()['update_seq']
			
	def __del__(self):
		EndContinuousUpdate(self)


	def UpdateData(self,feed='longpoll'):
		'''
			Updates data and erases data out of time range
			Note: by default, long polls so it will not return until something
			other feed options are normal, or continuous.  I have no idea
			what continuous would do in this situation.
			has changed
		'''
		changes=self._cmd.changes(since=self.last_seq,feed=feed)
		self.last_seq=changes['last_seq']
		for changeset in changes['results']:
			thecmd=self._cmd[changeset['id']]
			for key in self.do_on_update:
				self.do_on_update[key](thecmd)
	
	def BeginContinuousUpdate(self):
		'''
			start updating data in a new thread
		'''
		self.continuous_logging=True
		self.p=threading.Thread(target=self.ContinuousUpdate)
		self.p.daemon=True
		self.p.start()
#		thread.start_new_thread(self.ContinuousUpdate,())

	def EndContinuousUpdate(self):
		self.continuous_logging=False
		self.p.join()


	def ContinuousUpdate(self):
		'''
			continuously update stuff.  Don't call this
		'''
		while self.continuous_logging:
			time.sleep(5)
			nchanges=self.UpdateData(feed='longpoll')
			mytime=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			print "command update at "+mytime
		print("done.  killing thread")
		thread.exit()

	def AddDoOnUpdate(self,mykey,myfunc):
		'''
			Add a function to be called when something updates
		'''
		self.do_on_update_mutex.acquire()
		self.do_on_update[mykey]=myfunc
		self.do_on_update_mutex.release()
