from config import *
import shutil
import sys
import os
import datetime
import subprocess
import time
import socket

#Get machine ip_address

host_name = socket.gethostname()
my_ip= socket.gethostbyname(host_name) 


#release function start

def release():
    archive = "C:\\Archive\\"+ source.replace("C:\\","")+ datetime.datetime.now().strftime("%m-%d-%Y %H_%M_%S")
    shutil.copytree(destination,archive)    
    shutil.rmtree(destination)                                               

    shutil.copytree(source,destination)

    col_released.insert_one(released_data)

    col_release_on_queued.delete_one({"ip_address": my_ip})

    print("Successfully released")

#release function end



# python code that will run the release function -- Start

while True:
    #shutil.copytree('c:\\HelloWorld','z:\\delicious')
    #subprocess.check_output('net use y: /delete')
    today = datetime.datetime.now().replace(microsecond=0).isoformat(' ')


    check = col_release_on_queued.find({ "ip_address": my_ip })


    if check.count()>0:
        print("Match found for release")  

        
        for check in col_release_on_queued.find({ "ip_address": my_ip }):

            version = str(check["version"])
            acct_id = str(check["acct_id"])
            acct_code = str(check["acct_code"])
            released_data = {"ip_address": my_ip, "acct_id": acct_id, "acct_code": acct_code, "Status": "released", "Date_released": today }
                            
            source = "C:\\Release\\"+ version
            destination = "C:\\dev\\celery\\"+ version

            if not os.path.exists(source):
                print('source does not exist')
                exit()
                   #os.mkdir("C:\\Release\\"+ version)
                    
            if  os.path.exists(destination):
                release()
                
            else:
                os.makedirs(destination)
                release()
                      
    else:
        print("No match found: Waiting for release")

        
        #make celery_worker.py, make workerversion.bat
                




        #shutil.copytree('y:\\Titechadmin\\MyPython','c:\\dev\\cagol')
        
        
            

        #print(source,destination)

    time.sleep(10)

