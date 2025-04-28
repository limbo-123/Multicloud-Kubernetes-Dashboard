import time
import json

my_log_file = "/var/log/nginx/error.log"
error_msg = "500"
currenttime = []
error_count = []

with open(my_log_file, 'r') as errorfile:
    datafile = errorfile.read()
    for erros in datafile:
        if error_msg in erros:
            currenttime.append(time.time())
            error_count.append(error_msg.count())
            if currenttime > currenttime + 5:
                print("Error is there")
            while currenttime < currenttime - 5 and error_count.count > 10:
                print('Error reported')
            
            

