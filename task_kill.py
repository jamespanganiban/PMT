import os
import sys
import win32com.shell.shell as shell
import pymongo
import socket
import time
from config import * #config.py: database connection

host_name = socket.gethostname()
get_ip= socket.gethostbyname(host_name) 

#myclient = pymongo.MongoClient('mongodb://localhost:27017/')
#mydb = myclient["db_worker"]
#mycol = mydb["tbl_task_kill_on_queued"]
#mycol1 = mydb["tbl_killed_task"]


#GET all the process that need to kill matching the host IP_address 

while True:
    for doc in col_task_kill_on_queued.find():
        text = str(doc['PID'])
        filter_ip = str(doc['ip_address'])
        myquery = { "PID": text }
        if  (filter_ip == get_ip):
            for killed in col_task_kill_on_queued.find():
                pc_name = str(killed['pc_name'])
                ip_address = str(killed['ip_address'])
                date_time = str(killed['date/time'])
                PID = str(killed['PID'])
                window_title = str(killed['window_title'])
                status = "KILLED"

                move_on_ttk = { "pc_name": pc_name, "ip_address": ip_address,"date/time": date_time,"PID": PID,"window_title": window_title,"status": status }
                moved = col_killed_task.insert_one(move_on_ttk)

            print("Killing task from " + get_ip)
            print(text)
            os.system("taskkill /F /pid " + text)      
            col_task_kill_on_queued.delete_one(myquery)
            
#Add the killed task in tbl_killed_task
    

    time.sleep(1)