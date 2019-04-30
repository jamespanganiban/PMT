from config import *
import datetime
import socket
import os
from subprocess import check_output
import subprocess
import csv
import json
import time


#Get the ip address of the host/pc
host_name = socket.gethostname()
get_ip= socket.gethostbyname(host_name) 

while True:
	col_tasklist.delete_many({ "ip_address": get_ip })
				
	#Get the date/time today
	today = datetime.datetime.now().replace(microsecond=0).isoformat(' ')




	#cmd command that will get the tasklist
	var = subprocess.check_output('tasklist /v /fo csv /nh', universal_newlines = True)
	status = "Running"



	lines = var.split("\n")
	csvlines = csv.reader(lines)

	#Tasklogger: save the computer tasklist in the database (mongoDB)

	for line in csvlines:
			if len(line) > 0:

				data = line[6] 	
				data5 = get_ip		
				data3 = today
				data2 = line[1]
				data4 = line[8]
				data6 = status	
				current_list = [data,data5,data3,data2,data4,data6]
				

				#data4.find('Worker_') >= 0

			
			if data !="N/A" and data5 !="N/A" and data3 !="N/A" and data2 !="N/A" and data4 !="N/A":
				

				task_data = { "pc_name": data, "ip_address": data5,"date/time": data3,"PID": data2,"window_title": data4,"status": data6 }
				

				#check if the task is existing (to avoid data insertion duplicates)
				result = col_tasklist.find({"window_title": data4}) 
				if result.count() > 0:  
					newvalues ={ "$set": {"PID":  data2}}
					col_tasklist.update_one(task_data,newvalues)
				else:
					col_tasklist.insert_one(task_data)
					print("New task added from " + data5,": " + data4)
					
					#Move all data to history the delete the original data
					result2 = col_t_history.find({"PID": data2}) 
					if result2.count() > 0:
						print("")
					else:
						col_t_history.insert_one(task_data)

					

				#check if the ip is added or existing (for tbl_running_appsvr)
				check_appsvr = col_running_appsvr.find({"ip_address": data5}) 
				check_tasklist = col_tasklist.find({"ip_address": data5}) 
				if check_appsvr.count() > 0: 
					x = "test"
				else:
					if check_tasklist.count() > 0:
						running_appsvr = { "pc_name": data, "ip_address": data5, "date_time": data3 }
						col_running_appsvr.insert_one(running_appsvr)
						print ("New running app server added: " + data5 )
					else:
						delete_appsvr = { "ip_address": data5}
						col_running_appsvr.delete_one(delete_appsvr)
						print ("app running in" +  data5," has been stopped")

						


				
	time.sleep(10)		
	


	
