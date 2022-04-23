from asyncio.windows_events import NULL
import threading
import time
from PIL import ImageGrab
from PIL import ImageChops
import os
import tkinter
import keyboard

import diffcompare


#global snap_intrval
#global flag_threadexit


snap_intrval    = 10
flag_threadexit = 0
keyboard_key    = NULL

class th_getkey(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name     = name
    def run(self):
        global keyboard_key
        global flag_threadexit
        while(flag_threadexit == 0):
            time.sleep(1)
            if keyboard_key == NULL:
                keyboard_key = keyboard.read_key()

class th_snapshot(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name     = name

    def run(self):
        autosnapshot()    


def snapsave(curtime, imgcur):
    filename=os.path.abspath(".") + "\\imgsave\\" + \
        str(time.localtime(curtime).tm_mon).rjust(2,'0') + \
        str(time.localtime(curtime).tm_mday).rjust(2,'0') + "-" +\
        str(time.localtime(curtime).tm_hour).rjust(2,'0')+ \
        str(time.localtime(curtime).tm_min).rjust(2,'0') + "-" +\
        str(time.localtime(curtime).tm_sec).rjust(2,'0')+ \
        ".jpg"
    imgcur.save(filename)

def autosnapshot():
    global snap_intrval
    global keyboard_key
    global flag_threadexit
    ltime = time.time()
    #print(time.localtime(ltime).tm_hour)
    #print(ltime)
    i=0
    imglast=NULL
    scr_w=tkinter.Tk().winfo_screenwidth()
    scr_h=tkinter.Tk().winfo_screenheight()

    print(scr_w, scr_h)
    size=(0,0,scr_w,scr_h)
    start=0
    while(1):#(i<3):
        curtime = time.time()
        time.sleep(1)
        #add start stop control
        if keyboard_key != NULL:
            key=keyboard_key
            keyboard_key = NULL

            print(key)

            if key == '-':
                print("stop capture!")
                start=0
            elif key == '=':
                print("start capture!")
                start=1
            elif key == '\\':
                print("program stop now !!!")
                flag_threadexit = 1
                break

        if start == 0:
            ltime = curtime
        
        #print(ctime-ltime)
        if(curtime - ltime < snap_intrval):
            continue

        ltime = curtime
        #now capture the screen
        imgcur=ImageGrab.grab(size)
        if(imglast):
            #imgdiff=ImageChops.difference(imgcur, imglast)
            #imgdiff.show()
            #compare with preview picture
            #print(imgdiff.getbbox())
            #if(imgdiff.getbbox()):
            #    x1, y1, x2, y2 = imgdiff.getbbox()
            #    imgdiff=abs((x2-x1)*(y2-y1))*100.0/scr_w/scr_h
            #    print("box diff is %0.2f" %(imgdiff))

            imgdiff = diffcompare.classify_hist_with_split(imgcur, imglast)
            imgdiff = imgdiff * 100
            print("his diff is %0.2f" %(imgdiff))


            #save img
            if(imgdiff<98):
                snapsave(curtime, imgcur)
                imglast=imgcur
        else:
            snapsave(curtime, imgcur)
            imglast = imgcur

        
        #time.sleep(5)
        #i+=1




#main entrance
if __name__ == '__main__':
    threads = []

    thread1 = th_getkey("ThreadGetKey", 1)
    thread2 = th_snapshot("ThreadSnapShort", 2)

    thread1.start()
    thread2.start()

    threads.append(thread1)
    threads.append(thread2)

    for t in threads:
        t.join()

    print("completed exit!!")
