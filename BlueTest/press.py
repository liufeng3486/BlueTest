import requests
import threading
import time,random
import BlueTest

class SoloPress(threading.Thread):
    def file_write(self,path, temp):
        temp = str(time.time())+"\t"+temp
        with open("./result/" + str(path), "a+", encoding='utf8') as file:
            file.write(temp + "\n")
    def __init__(self,lock,index="",path="",count=100):
        threading.Thread.__init__(self)
        if not path:
            path = "./result/%s.txt"%str(index)
        if not index:
            index = self.name.split("-")[-1]
        self.index = index
        self.path = path
        self.count = count
        self.lock = lock
    def setup(self):
        pass

    def runcase(self):
        pass
    def precentCount(self,i):
        try:
            return int(((i+1)/(self.count))*100)
        except:
            return 100
    def run(self):
        percent = self.precentCount(0)
        for i in range(self.count):
            try:
                if self.precentCount(i) != percent:
                    if self.lock.acquire():
                        percent =  self.precentCount(i)
                        print ("index:%s, run:%d%% ,num:%d"%(self.index,percent,i+1))
                    self.lock.release()
                self.runcase()
            except Exception as es:
                self.file_write(self.index,str(es))

class Press(object):
    def __init__(self,num,step=1):
        self.num = num
        self.step = step
    def setup(self,solo_thread,index):
        solo_thread.setup(index)

    def run(self,solopress):
        ThreadList = []
        lock = threading.Lock()
        for i in range(1, self.num+1):
            t = solopress(lock,i)
            t.setup()
            ThreadList.append(t)
        for t in ThreadList:
            t.start()
        for t in ThreadList:
            t.join()
        print("fuck")


if "__main__" == __name__:
    class press_2(SoloPress):
        def setup(self):
            self.num = self.index
        def runcase(self):
            print (self.name,self.num)


    press= Press(2)
    press.run(press_2)

