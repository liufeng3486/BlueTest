import csv,re,os,copy
# import toolbox
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
mkdir("./log/")
mkdir("./result/")
mkdir("./srcdata/")
from BlueTest.logInit import *
from BlueTest.parm import *



class Postman2Csv(object):

    def __init__(self,path,resultpath="./srcdata/temp.csv"):
        self.path = path
        self.resultpath = resultpath #结果路径
        self.header = csv_parm.CHINA_KEY #中文key
        self.key =  csv_parm.KEY #key
    def run(self):
        # try:
            data = self.getData()
            self.write2Csv(data)
            log.logger.info("postman转csv成功:%s"%self.resultpath)
        # except Exception as es:
        #     log.logger.error("postman转csv失败")
        #     log.logger.error(es)

    def csvWrite(self,data): #写单行
        with open(self.resultpath, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile,dialect='excel')
            spamwriter.writerow(data)

    def printCsv(self): #打印csv现有内容
        with open(self.path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))

    def write2Csv(self,data): #根据数据写入csv
        self.csvWrite(self.header)
        for solo_data in data:
            self.csvWrite([PostParm.START]) #START标志位
            self.csvWrite(self.key)     #英文标签
            self.csvWrite(solo_data)    #数据
            self.csvWrite([PostParm.END]) #END标志位

    def getData(self,Cookie=False): #从postman获取数据
        false = PostParm.FALSE    #初始化特殊字符
        true = PostParm.TRUE
        null = PostParm.NULL
        with open(self.path,"r",encoding='utf8') as file: #读取文件会获取dict格式
            data = file.read()
            data = eval(data)[PostParm.REQUESTS]
        all_data = []
        for solo_data in data: #便利数据
            url = solo_data[PostParm.URL]
            url_list  = url.split("?")[0].split("/") #拆解url 获取path路径list
            url_parm = ""
            if len(url.split("?"))>1:   #包含? 增加 url params
                url_parm = url.split("?")[-1]
            url = url.split("?")[0] #去除?后内容
            try:
                error_headers = re.findall("\n//.*", solo_data[PostParm.HEADERS])  # //是为了处理postman 中被注释的数据
                if error_headers:
                    for error_header in error_headers:
                        solo_data[PostParm.HEADERS] = solo_data[PostParm.HEADERS].replace(error_header, "")
            except Exception as es:
                log.logger.error(es)

            if not Cookie:  #不需要cookie
                try:
                    cookies = re.findall("Cookie.*",solo_data[PostParm.HEADERS])  #正则并删除cookie
                    if cookies:
                        for cookie in cookies:
                            solo_data[PostParm.HEADERS] = solo_data[PostParm.HEADERS].replace(cookie,"")
                except Exception as es:
                    log.logger.error(es)
            #组装数据
            temp_list = ["", #lv
                         "", #Cname
                         url_list[-1], #name
                         solo_data[PostParm.NAME], #Describe
                         "./"+url_list[-2]+"/"+url_list[-1],#ResualPath
                         solo_data[PostParm.METHOD],#method
                         url, #url
                         solo_data[PostParm.HEADERS],#headers
                         solo_data[PostParm.DATA],#data
                         solo_data[PostParm.DATATYPE],#datatype
                         url_parm,  # UrlParams
                         "" #TestType
                        ]
            if temp_list[code_parm.DATATYPE]==csv_parm.RAW:
                temp_list[code_parm.DATA] = solo_data[PostParm.RAWMODEDATA]
            all_data.append(temp_list)
        return all_data
from BlueTest.logInit import *
class Csv2Dict(object):

    def __init__(self,path="./data/temp.csv",debug=False):

        self.debug = debug
        self.path = path
        self.key =  csv_parm.KEY #key
    def run(self):

        if self.debug:
            data = self.readAll()
            dict_data = self.list2Dict(data)
            log.logger.debug("CSV文件内容序列化成功:%s",str(dict_data))
            return dict_data
        else:
            try:
                data = self.readAll()
                dict_data = self.list2Dict(data)
                log.logger.debug("CSV文件内容序列化成功:%s", str(dict_data))
                return dict_data
            except Exception as ex:
                log.logger.error("CSV文件内容序列化失败:%s", str(ex))
                return False

    def urlParamsDo(self,urlparams_string):
        if urlparams_string:
            urlparams = {}
            params_list = urlparams_string.split("&")

            for solo_param in params_list:
                urlparams[solo_param.split("=")[0]]=solo_param.split("=")[1]
            return urlparams
        return urlparams_string
    def dataParamsDo(self,data):
        if len(data)>4:
            data = eval(data)
            body = {}
            for solo_data in data:
                body[solo_data["key"]] = solo_data["value"]
            return body
        return  data

    def readAll(self):

        print ("readall")
        try:
            temp_list = []
            with open(self.path, newline='',encoding='utf8') as csvfile:
                spamreader = csv.reader(csvfile,dialect='excel')
                for solo in spamreader:
                    temp_list.append(solo)
            return temp_list
        except Exception as es:
            log.logger.debug("CSV文件内容utf8序列化失败重试:%s", str(es))
        try:
            temp_list = []
            with open(self.path, newline='') as csvfile:
                spamreader = csv.reader(csvfile,dialect='excel')
                for solo in spamreader:
                    temp_list.append(solo)
            return temp_list
        except Exception as es:
            log.logger.debug("CSV文件内容序列化失败:%s",str(es))

    def list2Dict(self,data):
        data_temp = []
        start_list = []
        for index,value in enumerate(data):
            if not value:
                continue
            if value == [PostParm.START] or value[0] == PostParm.START:
                start_list.append(index)
        for index in start_list:
            solo_data = {}
            for sub_index,key in enumerate(data[index+1]):
                solo_data[key] = data[index+2][sub_index]
            solo_data[csv_parm.HEADERS] = self.header2Dict(solo_data[csv_parm.HEADERS])
            solo_data[csv_parm.URLPARAMS] = self.urlParamsDo(solo_data[csv_parm.URLPARAMS] )
            if solo_data[csv_parm.DATATYPE] != RAW:
                solo_data[csv_parm.DATA] = self.dataParamsDo(solo_data[csv_parm.DATA])
            data_temp.append(solo_data)
        return data_temp
    def header2Dict(self,header_string):
        while header_string[-1] == "\n":
            header_string =  header_string[:-1]
        header_string =  '\''+header_string+'\''
        header_string = header_string.replace("\n","\',\'")
        header_string = header_string.replace(":", "\':\'")
        header_string = header_string.replace("http\':\'//","http://")
        header_string = header_string.replace("https\':\'//", "https://")
        header_string = '{'+header_string+'}'
        header_dict = eval(header_string)
        return header_dict
class dict2Py(object):
    def __init__(self,data=""):
        self.data = data
        self.tab = 0
        self.path = './srcdata/'+data[csv_parm.RESUALPATH].split("/")[1]
        self.mkdir(self.path)
        data[csv_parm.RESUALPATH] = './srcdata/' + data[csv_parm.RESUALPATH] +".py"

    def mkdir(self,path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
    def setup(self):
        pass


    def write(self,data):
        with open(self.data[csv_parm.RESUALPATH],"a",encoding='utf8') as file:
            file.write("\t"*self.tab+data+"\n\n")
    def mkpy(self):
        querystring = False
        payload = False
        self.write("import requests")
        self.write('url = "%s"'%self.data[csv_parm.URL])
        if self.data[csv_parm.URLPARAMS]:
            self.write('querystring = %s'%self.data[csv_parm.URLPARAMS])
            querystring = True
        if self.data[csv_parm.DATA] != "null":
            self.write("payload = %s"%self.data[csv_parm.DATA])
            payload = True
        header_temp = "headers =%s"%self.data[csv_parm.HEADERS]
        header_temp = header_temp.replace("\',","\',\n\t")
        self.write(header_temp)
        request_temp = 'response = requests.request("%s", url,'

        if querystring:
            request_temp += " params=querystring,"
        if payload:
            request_temp += "data=payload,"
        self.write(request_temp%self.data[csv_parm.METHOD]+")")

        self.write('print(response.text)')

class Base(object):
    def __init__(self):
        self.temp_map = []

    def list_dictionary(self,dictionary, key_list=[]):
        if type(dictionary) == type({}):
            for key, value in dictionary.items():
                self.temp_map.append(key)
                if type(value) == type([]) or type(value) == type({}):
                    self.list_dictionary(value, key_list)
                else:
                    key_list.append(copy.copy(self.temp_map))
                    self.temp_map = self.temp_map[:-1]
        elif type(dictionary) == type([]):
            for key, value in enumerate(dictionary):
                self.temp_map.append(key)
                if type(value) == type([]) or type(value) == type({}):
                    self.list_dictionary(value, key_list)
                else:
                    key_list.append(copy.copy(self.temp_map))
                    self.temp_map = self.temp_map[:-1]
        self.temp_map = self.temp_map[:-1]
        return key_list

    def getValue(self,data, key_list):
        self.temp_map = []
        res_key_list = []
        value_list = []
        for key in key_list:
            for index, value in enumerate(key):
                if index == 0:
                    solo = data[value]
                else:
                    solo = solo[value]
            res_key_list.append(key)
            value_list.append(solo)
        return res_key_list, value_list
    def dataGetKeyAndValue(self,dictionary):
        self.temp_map=[]
        key_list = self.list_dictionary(dictionary,[])
        return self.getValue(dictionary,key_list)



if __name__ == '__main__':

    pass
