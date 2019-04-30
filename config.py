import pymongo

#13.229.17.45 Live mongoDB server public IP address
#10.60.10.207 Live mongodDB server local IP address
#192.168.221.21 - test mongoDB server local IP address 

try:
    #myclient = pymongo.MongoClient('mongodb://192.168.221.30:27017/27017') #James-PC server
    myclient = pymongo.MongoClient('mongodb://admin:titechadmin@192.168.221.101:27017/?authSource=db_tasklist')
    #myclient = pymongo.MongoClient('mongodb://admin:titechadmin@13.229.17.45:27017/?authSource=admin') #Live mongoDB server
except pymongo.errors.ConnectionFailure as msg:
    print ("Failed connection: %s" % str(msg))

#db = myclient["db_worker"] # Free live/Live mongoDB server tasklist database
db = myclient["db_tasklist"] #local mongoDB server tasklist database
col_tasklist = db["tbl_tasklist"] 
col_t_history = db["tbl_tasklist_history"]
col_running_appsvr = db['tbl_running_appsvr']
col_task_kill_on_queued = db["tbl_task_kill_on_queued"]
col_killed_task = db["tbl_killed_task"]

#collection for release
col_release_on_queued = db["tbl_release_on_queued"]
col_released = db['tbl_released']