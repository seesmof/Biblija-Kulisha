import os 
import time 

ORIGINAL_BIBLE=os.path.join(os.path.dirname(os.path.abspath(__file__)),"Original")
target_file=os.path.join(ORIGINAL_BIBLE,"43LUKBKS.USFM")

last_time=os.path.getmtime(target_file)
while 1:
    cur_time=os.path.getmtime(target_file)
    if cur_time!=last_time:
        print("CHECK")
        last_time=cur_time
    time.sleep(1)
