# coding: utf8

import os
import sys
import time
import datetime
from datetime import date,timedelta
import shutil
import sched

schedule = sched.scheduler(time.time, time.sleep)
start_time = 0
end_time = 0
interval = 60 

class mytimer(object):
	# 在该方法中实现了循环，将path1路径下的内容拷贝到path2中去
	def execute_command(self, path1, path2, inc):
		# print(path1)
		print(path2)
		start_time = datetime.datetime.now()
		self.change(path1,path2)
		end_time = datetime.datetime.now()

		delay = round((end_time-start_time).total_seconds()) 
		print(u'开始时间：%s' % start_time)
		print(u'耗时:%s秒' %(delay))

		#获取新的地址，进行下一次拷贝
		newSor = path1[:-8] + self.getTodaySourcePath()
		newDes = path2[:-8] + self.getTodaySourcePath()

		schedule.enter(int(inc-delay), 0, self.execute_command, (newSor,newDes,inc))
		print (u'结束时间：%s' % end_time)

	#该函数主要用于确定第一次运行的时间，引出后续的循环运行	
	def cmd_timer(self,path1,path2,time_str,inc):
		now = datetime.datetime.now()
		schedule_time = datetime.datetime.strptime(time_str,'%H:%M').replace(year=now.year,month=now.month,day=now.day)
		if schedule_time < now:
			schedule_time = schedule_time + datetime.timedelta(days=1)
		time_before_start = int(round((schedule_time-datetime.datetime.now()).total_seconds()))
		print (u'mytimer => 还有%s秒开始任务' %time_before_start)
		schedule.enter(time_before_start, 0, self.execute_command, (path1,path2,inc))
		schedule.run()	

	def change(self,path1,path2):
		'''
		先判断资源地址是否存在，不存在则不拷贝；
		#接着判断目标地址是否存在，不存在则创建
		'''
		isExistSor = os.path.exists(path1)
		if isExistSor:
			print("资源文件存在，开始拷贝")
			self.mkdir(path2)		
			self.copy(path1,path2)
		else:
			print("资源文件不存在！！")	

				
	def copy(self,path1,path2):
		for theFile in os.listdir(path1):
			if os.path.isfile(path1 + os.path.sep + theFile):
				#1->2
    			#现在theFile是文件
				shutil.copy(path1 + os.sep + theFile, path2) 
			elif os.path.isdir(path1 + os.path.sep + theFile):
				#现在theFile是文件夹
				self.mkdir(path2 + os.path.sep + theFile)
				self.change(path1 + os.sep + theFile, path2 + os.path.sep + theFile)				
						
	def mkdir(self,path):
		print("1111")
		folder = os.path.exists(path)
		if not folder:
			os.makedirs(path)
			print("创建成功！")
		else:
			print("目标文件夹已经存在！")	

	def getYesterdaySourcePath(self):
		today = date.today()
		# print(today)
		yesterday = today + timedelta(days = -1)
		# print(yesterday)
		str_yesterday = str(yesterday)
		# print(type(str_yesterday))
		str_ytd = str_yesterday[0:4] + str_yesterday[5:7]+ str_yesterday[-2:]
		# print(str_ytd)	
		return str_ytd

	def getTodaySourcePath(self):
		today = str(date.today())
		str_td = today[0:4] + today[5:7]+ today[-2:]
		return str_td

if __name__ == '__main__':     
    path1 = '/Users/diver/Desktop/file1/'
    # path1 = '/Volumes/AOI\x20DATA/test/'
    path2 = '/Users/diver/Desktop/file2/test/'
    mytimer = mytimer()
    timePath = mytimer.getYesterdaySourcePath()
    sourcePath = path1 + timePath
    destinationPath = path2 + timePath
    # print(sourcePath)
    # print(destinationPath)
    mytimer.cmd_timer(sourcePath,destinationPath,'9:46',interval)            
        
	