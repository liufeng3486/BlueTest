import requests
import threading
import time,random
from BlueTest.parm import *
import BlueTest.toolbox as toolbox
import datetime

class SoloPress(threading.Thread):

    def __init__(self,lock,index="",path="",count=100):
        threading.Thread.__init__(self)
        if not path:
            path = MainParam.Result_Path+MainParam.Press_File+str("presslog")+".log"
            # path = "./result/Press_%s.txt"%str(index)
        if not index:
            index = self.name.split("-")[-1]
        self.index = index
        self.path = path
        # self.path = path
        self.count = count
        self.lock = lock
        self.file = open(str(path), "a+", encoding='utf8')
    # def assertResponse(self,data):
    #     for error in self
    def file_write(self,*args):
        path = self.path
        temp = str(datetime.datetime.fromtimestamp(int(time.time())))+"\t"
        if self.lock.acquire():
            for solo in args:
                temp +="\t" + str(solo).replace("\n","")
            self.file.write(temp + "\n")
        self.lock.release()
        # with open(str(path), "a+", encoding='utf8') as file:
        #     file.write(temp + "\n")
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
                if self.precentCount(i) < 1:
                    print("index:%s, run:%.2f%% ,num:%d" % (self.index, int(((i+1)/(self.count))*10000)/100.0, i + 1))
                if self.precentCount(i) != percent :
                    if self.lock.acquire():
                        percent =  self.precentCount(i)
                        print ("index:%s, run:%d%% ,num:%d"%(self.index,percent,i+1))
                    self.lock.release()
                self.start = time.time()
                self.runcase()

                self.file_write(MainParam.USETIME+"_"+str(int((time.time()-self.start)*1000)))

            except Exception as es:
                self.file_write(str(self.index)+"\t"+str(es))

class Press(object):
    def __init__(self,num,step=1):
        self.num = num
        self.step = step
    def dataReduction(self,path = ""):
        if not path:
            path = MainParam.Result_Path +"Press_press.log"
        press_files = toolbox.getFilePath(path, spec_str=MainParam.Press_File)
        time_dict = {}
        temp_resualt_dict = {}
        resualt_dict = {}
        # for press_file in press_files:
        with open( path, "r", encoding='utf8') as file:
            for line in file.readlines():
                line = line.replace("\n", "")
                temp_list = line.split("\t")
                if MainParam.USETIME in  line:
                    for i in temp_list:
                        if MainParam.USETIME in i:
                            try:
                                time_dict[i.split("_")[-1]] += 1
                            except:
                                time_dict[i.split("_")[-1]] = 1
                if MainParam.RESPONSE_TRUE in line:
                    try:
                        temp_resualt_dict[temp_list[0]][0] += 1
                    except:
                        temp_resualt_dict[temp_list[0]] = [1, 0]
                if MainParam.RESPONSE_FALSE in line:
                    try:
                        temp_resualt_dict[temp_list[0]][1] += 1
                    except:
                        temp_resualt_dict[temp_list[0]] = [0, 1]
        for key, value in temp_resualt_dict.items():
            resualt_dict[key] = value
        resualt_path = MainParam.Result_Path+MainParam.RESUALT_CSV
        toolbox.csvWrite(MainParam.RRESS_RESUALT_HEADER,resualt_path)
        for key,value in resualt_dict.items():
            toolbox.csvWrite([key, value[0],value[1]], resualt_path)

        time_path = MainParam.Result_Path+MainParam.TIME_CSV
        toolbox.csvWrite(MainParam.PRESS_TIME_HEADER,time_path)
        for key,value in time_dict.items():
            toolbox.csvWrite([key, value], time_path)

        return resualt_dict, time_dict

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



if "__main__" == __name__:
    class press_2(SoloPress):
        def setup(self):
            self.num = self.index
        def runcase(self):
            print (self.name,self.num)


    press= Press(2)
    press.run(press_2)

