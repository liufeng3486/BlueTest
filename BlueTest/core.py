# Insert your code here.
#coding = utf8
from GreenTest.toolbox import *


from GreenTest.logInit import *
null="null"
import requests,random,time


class apiTest(object):
    def __init__(self,data):
        self.data = data
        self.min = 5
        self.max = 10000

    def recordResults(self,data):
        mkdir(".//result//")
        with open(".//result//data.txt","a",encoding='utf8') as file:
            file.write("%s \n"%(data))
        log.logger.info("%s \n"%(data))

    def soloRequest(self,body=False,urlparams=False):
        error_list = ["error","Error","False","false","失败","错误","异常","禁止"]
        time.sleep(1)

        querystring = False
        payload = False

        if self.data[csv_parm.URLPARAMS]:
            querystring = self.data[csv_parm.URLPARAMS]
        if urlparams:
            querystring = urlparams
        if self.data[csv_parm.DATA] != "null":
            payload = self.data[csv_parm.DATA]
        if body:
            payload = body
        if self.data[csv_parm.DATATYPE] == csv_parm.RAW: #处理raw格式数据
            payload = str(payload)
            payload = payload.replace(" '", "\"").replace("' ", "\"").replace("'", "\"")

        # with requests.request(method=self.method, url=self.url, params=body) as response:
        with requests.request(method=self.method,url=self.url, params=querystring,data=payload) as response :
            state = False
            for error in error_list:
                if error in response.text:
                        return False,response.text
            return True,response.text
    def specifyLength(self,spec_num=False):
        if not spec_num:
            low = self.min
            height = self.max
            mid =  int((low + height) / 2)
            # str(random.randint(10 ** mid, 10 ** (mid + 1)))
            # return int((low + height) / 2)
            return str(random.randint(10 ** mid, 10 ** (mid + 1)))
        else:
            return str(random.randint(10 ** spec_num, 10 ** (spec_num + 1)))
    def deepTemp(self,temp,value,key):
        str_temp = "temp"
        for index, ddd in enumerate(key):  # 置空
            str_temp += "[key[%d]]" % index
        str_temp += "=%s"%(str(value))
        exec(str_temp)

    def limitCheck(self,body,key,urlparams=False):
        temp = copy.deepcopy(body)
        self.deepTemp(temp,self.specifyLength(spec_num=100000),key)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(body=temp)


        self.deepTemp(temp, self.specifyLength(spec_num=1), key)
        if urlparams:
            spec_response_2 = self.soloRequest(urlparams = temp)
        else:
            spec_response_2 = self.soloRequest(body=temp)

        if spec_response_2 == spec_response:
            if urlparams:
                self.recordResults("%s urlparams %s:limit error >:%s " % (self.name, str(key), str(100000)))
                self.recordResults("%s \n"%str(spec_response_2[1]))
            else:
                self.recordResults("%s urlparams %s:limit error >:%s " % (self.name, str(key), str(100000)))
                self.recordResults("%s \n"%str(spec_response_2[1]))
            return True
        self.min = 1
        self.max = 100000
        while abs(self.min - self.max) > 1:
            temp_len = int((self.min + self.max) / 2)
            self.deepTemp(temp, self.specifyLength(), key)
            if urlparams:
                response = self.soloRequest(urlparams = temp)
            else:
                response = self.soloRequest(body=temp)

            log.logger.debug("key:%s max:%s min:%s cur:%s response:%s"%(key,str(self.max),str(self.min),str(temp_len),response))
            if response == spec_response:
                self.max = temp_len
            else:
                self.min = temp_len
        for i in range(self.max + 1, self.min - 2, -1):
            self.deepTemp(temp, self.specifyLength(spec_num=i), key)
            if urlparams:
                response = self.soloRequest(urlparams=temp)
            else:
                response = self.soloRequest(body = temp)
            log.logger.debug("finish check:%s response:%s"%(str(i+1),response))
            if response != spec_response:
                if urlparams:
                    self.recordResults("%s urlparams %s:limit:%s \n" % (self.name, str(key), str(i+1)))
                    self.recordResults("%s \n" % str(spec_response[1]))
                else:
                    self.recordResults("%s  %s:limit:%s \n" % (self.name, str(key), str(i+1)))
                    self.recordResults("%s \n" % str(spec_response[1]))
                return i
        return False

    # def exceptionCheck(self,body,key,data=""):
    #     temp2 = copy.copy(self.data)
    #
    #     temp = copy.copy(body)
    #     print ("key:",key)
    #     temp2[key] = ""
    #     spec_response = self.soloRequest(temp)
    #     self.recordResults("%s exceptionCheck: %s为空 response:%s"%(self.name,key,spec_response))
    #     temp.pop(key)
    #     spec_response = self.soloRequest(temp)
    #     self.recordResults("%s exceptionCheck: %s不传 response:%s" % (self.name,key, spec_response))

    def exceptionCheck(self, body, key, urlparams=False):

        temp = copy.deepcopy(body)
        str_temp="temp"
        for index,value in enumerate(key): #置空
            str_temp+="[key[%d]]"%index
        str_temp += "=\"\""
        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        self.recordResults("%s exceptionCheck: %s为空 response:%s" % (self.name, key, spec_response))
        str_temp = "temp"
        for index in range(len(key)-1):
            str_temp += "[key[%d]]" % index
        str_temp += ".pop(key[-1])"
        exec(str_temp)
        if urlparams:
            spec_response = self.soloRequest(urlparams = temp)
        else:
            spec_response = self.soloRequest(temp)
        log.logger.debug(temp)
        self.recordResults("%s exceptionCheck: %s不传 response:%s" % (self.name, key, spec_response))

    def dataReduction(self,data):
        self.headers = self.data[csv_parm.HEADERS]
        self.url = self.data[csv_parm.URL]
        self.method = self.data[csv_parm.METHOD]
        self.name = self.data[csv_parm.NAME]
        d = Base()
        if self.data[csv_parm.DATA] != "null" and self.data[csv_parm.METHOD] == "POST":
            body = self.data[csv_parm.DATA]
            try:
                body = eval(body)
            except:
                pass

            keys,values = d.dataGetKeyAndValue(body)

            for key in keys:
                self.exceptionCheck(body, key)
                for solo in range(3):
                    limit = self.limitCheck(body, key)
                    if limit:
                        break
        if type(self.data[csv_parm.URLPARAMS]) == type({}):
            body = self.data[csv_parm.URLPARAMS]
            keys, values = d.dataGetKeyAndValue(self.data[csv_parm.URLPARAMS])
            for key in keys:
                self.exceptionCheck(body, key,urlparams=True)
                for solo in range(3):
                    limit = self.limitCheck(body, key,urlparams=True)
                    if limit:
                        break

def initPostMan(name,result_path = ""):
    path = ""
    result_name = ""
    if "\\" in name or "/" in name or "//" in name:
        path = name
    if not result_path:
        if path:
            result_name = name.split("\\")[-1].split("//")[-1].split("/")[-1].split(".")[0]
        else:
            result_name = name.split(".")[0]
        result_path = "..\\srcdata\\%s.csv"%result_name

    if not path:
        test = Postman2Csv("..\\srcdata\\%s.json.postman_collection"%name,resultpath=result_path)
    else:
        test = Postman2Csv("..\\srcdata\\%s.json.postman_collection"%name,resultpath=result_path)
    print (
        result_path
    )
    test.run()
def testByCsvData(name,normal_test=True,mkpy=False):
    path = ""
    if "\\" in name or "/" in name or "//" in name:
        path = name
    if not path:
        test = Csv2Dict("..\\srcdata\\%s.csv"%name)
    else:
        test = Csv2Dict(path)
    d = test.run()
    if normal_test:
        for i in d:
            if mkpy:
                temp = dict2Py(data=i)
                temp.mkpy()
            test = apiTest(i)
            test.dataReduction(1)

import requests
requests.request()
if __name__ == '__main__':
    pass
    # initPostMan("ijx")
    # testByCsvData("ijx")
    # a = Csv2Dict(debug=True)
    # d = a.run()

    # test = Postman2Csv("..\\postmandata\\")
    # test.run()
    # a =  Csv2Dict(debug=True)
    # d = a.run()
    # for i in d:
    #     temp = dict2Py(data=i)
    #     # temp.mkpy()
    #     test = apiTest(i)
    #     test.dataReduction(1)
    # print (d)
    # for i in d:
    #     temp = dict2Py(data = i)
    #     temp.mkpy()

    # d = dict2Py(data = d[0])
    # d.mkpy()
    #
    #
    #
    # a =  Csv2Dict(debug=True)
    # d = a.run()
    # print (d )
    # test = apiTest(d[2])
    # # print (test.data)
    # test.dataReduction(1)
    # test.getData(".\\postmandata\\ijx.json.postman_collection")

