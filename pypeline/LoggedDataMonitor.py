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
import threading

class LoggedDataMonitor:
	'''
		Class that monitors recent data from Couchdb
	'''
	def __init__(self, couch_url="http://127.0.0.1:5984"):
		'''
			Connects to data server and looks for logged data.
			Inputs:
			<couch_url> (string) URL of CouchDB server
		'''
		print "connecting to database"
		self._server = CouchServer(couch_url)
		if (self._server.__contains__('dripline_logged_data')):
			self._logged_data = self._server['dripline_logged_data']
		else:
			raise UserWarning('The dripline logged data database was not found!')
		#some defaults and internal variables
		self.continuous_logging=False
		self.do_on_update={}
		self.do_on_update_mutex=threading.Lock()
		self.data_mutex=threading.Lock()
		#by default, load data from the last three hours
		self.timescale_hours=3;
		print "loading last "+str(self.timescale_hours)+" hours of data"
		self.last_seq=self._logged_data.info()['update_seq']
		start_time=datetime.today()-timedelta(hours=self.timescale_hours);
		#actually load the data
		self.times={}
		self.values={}
		self.units={}
		mystartkey=start_time.strftime("%Y-%m-%d %H:%M:%S")
		myendkey=datetime.today().strftime("%Y-%m-%d %H:%M:%S")
		print "mystartkey is "+mystartkey
		print "myendkey is "+myendkey
		thedata=self._logged_data.view('log_access/all_logged_data',startkey=start_time.strftime("%Y-%m-%d %H:%M:%S"),endkey=myendkey)
		print "number of entries: "+str(len(thedata))
		for row in thedata:
			self.EatDocument(row.value)
		self.logfile=open("mylog.txt",'w+')
	
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
		changes=self._logged_data.changes(since=self.last_seq,feed=feed)
		self.last_seq=changes['last_seq']
		for changeset in changes['results']:
			self.EatDocument(self._logged_data[changeset['id']])
		#print "update with "+str(len(changes['results']))+" additions"
		start_time=datetime.today()-timedelta(hours=self.timescale_hours);
		removals=0
		for sensor in self.times:
			while len(self.times[sensor][0])>0 and datetime.strptime(self.times[sensor][0],"%Y-%m-%d %H:%M:%S")<start_time:
				self.times[sensor].pop(0)
				self.values[sensor].pop(0)
				removals=removals+1
		return len(changes['results'])+removals
		#print str(removals)+" deletions"
	
	def EatDocument(self,doc):
		'''
			Ingest a document into the data store
		'''
		self.data_mutex.acquire()
		sensor=doc['sensor_name']
		if self.times.get(sensor)==None:
			self.times[sensor]=[]
			self.values[sensor]=[]
		self.times[sensor].append(doc['timestamp_localstring'])
		self.values[sensor].append(doc['calibrated_value'].split()[0])
		self.units[sensor]=doc['calibrated_value'].split()[1]
		self.data_mutex.release()

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
			print "update at "+mytime
			if nchanges!=0:
				self.do_on_update_mutex.acquire()
				for key in self.do_on_update:
					self.do_on_update[key]()
				self.do_on_update_mutex.release()
		print("done.  killing thread")
		thread.exit()

	def AddDoOnUpdate(self,mykey,myfunc):
		'''
			Add a function to be called when something updates
		'''
		self.do_on_update_mutex.acquire()
		self.do_on_update[mykey]=myfunc
		self.do_on_update_mutex.release()
	
	def GetTimeAndValues(self,sensor):
		self.data_mutex.acquire()
		ret=zip(self.times[sensor],self.values[sensor])
		self.data_mutex.release()
		return ret

	def GetUnits(self,sensor):
		self.data_mutex.acquire()
		ret=self.units[sensor]
		self.data_mutex.release()
		return ret

	def GetSensors(self):
		ret = []
		for sensor in self.times:
			ret.append(sensor)
		return ret
