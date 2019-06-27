import csv,re,os,copy,shutil
import datetime
# from Crypto import Random
# from Crypto.PublicKey import RSA  #https = http+ssl  ssl = rsa
# from Crypto.Cipher import PKCS1_v1_5

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

    def __init__(self,path,resultpath="./srcdata/temp.csv",encode=""):
        self.path = path
        self.resultpath = resultpath #结果路径
        self.header = csv_parm.CHINA_KEY #中文key
        self.key =  csv_parm.KEY #key
        self.encode = encode


    def run(self):
        # try:
            data = self.getData() #数据结构确定
            self.write2Csv(data) 
            log.logger.info("postman转csv成功:%s"%self.resultpath)
        # except Exception as es:
        #     log.logger.error("postman转csv失败")
        #     log.logger.error(es)

    def csvWrite(self,data): #写单行
        if self.encode:
            with open(self.resultpath, 'a', newline='',encoding=self.encode) as csvfile:
                spamwriter = csv.writer(csvfile, dialect='excel')
                spamwriter.writerow(data)
        else:
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

        src_datas = []
        with open(self.path,"r",encoding='utf8') as file: #读取文件会获取dict格式
            data = file.read()

            data = data.replace("[]","\"\"")

            data = data.replace(": ",":")



            try:
                src_datas = eval(data)[PostParm.REQUESTS]
            except:
                try:
                    data_temp = eval(data)["item"]
                    for solo in data_temp:
                        data_use = solo
                        
                        data = data_use[PostParm.REQUEST]
                        
                        data[PostParm.URL]=data["url"]["raw"]
                        if "https" not in data[PostParm.URL]:
                            data[PostParm.URL] = "http://" + data[PostParm.URL]
                        
                        data["name"] = data_use["name"]
                        data["headers"]=data["header"]
                        data["data"] = data["body"][data["body"]["mode"]]
                        data[PostParm.DATATYPE] = data["body"]["mode"]
                        data[PostParm.RAWMODEDATA] = data["data"]
                        src_datas.append(data)

                except:
                    raise "data error"
        all_data = []
        # src_datas = [data,]
        for solo_data in src_datas: #便利数据
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
            # try:
                data = self.readAll()
                print(data)
                dict_data = self.list2Dict(data)
                log.logger.debug("CSV文件内容序列化成功:%s", str(dict_data))
                return dict_data
            # except Exception as ex:
            #     log.logger.error("CSV文件内容序列化失败:%s", str(ex))
            #     return False

    def urlParamsDo(self,urlparams_string):
        if urlparams_string:
            urlparams = {}
            params_list = urlparams_string.split("&")

            for solo_param in params_list:
                # print(solo_param)
                if("="not in solo_param):
                    solo_param += "="
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
            with open(self.path, newline='',encoding='utf-8') as csvfile:
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
            # print(index,start_list)
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
        try:
            while header_string[-1] == "\n":
                header_string =  header_string[:-1]

            if "[" == header_string[0] and "]"== header_string[-1]:
                header_new = eval(header_string)
                header_temp = {}
                for solo in header_new:
                    header_temp[solo["key"]] = solo["value"]
                return header_temp


            header_string =  '\''+header_string+'\''
            header_string = header_string.replace("\n","\',\'")
            header_string = header_string.replace(":", "\':\'")
            header_string = header_string.replace("http\':\'//","http://")
            header_string = header_string.replace("https\':\'//", "https://")
            header_string = '{'+header_string+'}'
            header_dict = eval(header_string)
            return header_dict
        except:
            return {}
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
    @staticmethod
    def executeCatch(fun):
        def add_cap(*args, **kwargs):
            try:
                fun(*args, **kwargs)
            except Exception as ex:
                print('Error execute: %s' % fun.__name__)
                print('Exception: %s' % ex)
                print(kwargs)
                return False
        return add_cap

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

#1返回当前目录下非目录子文件 , spec_str 符合特定规则
def getFilePath(path,mode=1,spec_str=""):
    if mode == 1:
        for root, dirs, files in os.walk(path):
            if root == path:
            # print(root, end=' ')  # 当前目录路径
            # print(dirs, end=' ')  # 当前路径下的所有子目录
                if  spec_str:
                    temp_files = []
                    for file in files:
                        if spec_str in file:
                            temp_files.append(file)
                    return temp_files
                else:
                    return(files)  # 当前目录下的所有非目录子文件
    else:
        raise "mode error"

#csv写单行
def csvWrite(data,path): #写单行
    with open(path, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile,dialect='excel')
        spamwriter.writerow(data)
#打印csv内容
def printCsv(path): #打印csv现有内容
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
def responseAssert(data,error_list=MainParam.ERROR_LIST):
    for error in error_list:
        if error in str(data):
            return "RESPONSE_FALSE"
    return "RESPONSE_TRUE"

import datetime
class ToolBox(object):
    class TimeBox(object):
        @staticmethod
        def test2():
            print (self.test)
        @staticmethod
        def timetime2datetime(time_time):
            return datetime.datetime.fromtimestamp(time.time())
        @staticmethod
        def datetimePlus(src_datetime,**kwargs): # 对时间增加某个增量
            plus = datetime.timedelta(**kwargs)
            src_datetime += plus
            return src_datetime
    class RequestBox(object):
        @staticmethod
        def responseAssert(data, error_list=MainParam.ERROR_LIST):
            for error in error_list:
                if error in str(data):
                    return "RESPONSE_FALSE"
            return "RESPONSE_TRUE"
    class CsvBox(object):
        @staticmethod
        def printCsv(path):  # 打印csv现有内容
            with open(path, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    print(', '.join(row))
        @staticmethod
        def csvWrite(data, path):  # 写单行
            with open(path, 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, dialect='excel')
                spamwriter.writerow(data)
    class FileBox(object):
        @staticmethod
        def getFilePath(path, mode=1, spec_str=""):
            #mode 1 当前目录下的所有非目录子文件
            if mode == 1:
                for root, dirs, files in os.walk(path):
                    if root == path:
                        if spec_str:
                            temp_files = []
                            for file in files:
                                if spec_str in file:
                                    temp_files.append(file)
                            return temp_files
                        else:
                            return (files)
            else:
                raise "mode error"
        @staticmethod
        def fileCopy(src,des):
            shutil.copyfile(src, des)



    class RsaFile:
        def creatKeys(private="private.pem", public="public.pem"):
            random_generator = Random.new().read
            rsa = RSA.generate(1024, random_generator)
            private_pem = rsa.exportKey()
            public_pem = rsa.publickey().exportKey()
            with open(private, 'wb') as file:
                file.write(private_pem)
            with open(public, 'wb') as file:
                file.write(public_pem)

        def rsaEncrypt(key_path, soure_file, enccrypt_file="Encrypt", length=100):
            with open(key_path, "r") as f:
                key = f.read()
                key = RSA.importKey(key)
                key = PKCS1_v1_5.new(key)
            res = []
            with open(soure_file, "rb") as file:
                msg = file.read()
                for i in range(0, len(msg), length):
                    res.append(key.encrypt(msg[i:i + length]))
            with open(enccrypt_file, "wb") as file:
                for i in res:
                    file.write(i)
            return True

        def rsaDecrypt(key_path, soure_file, decrypt_file, length=128):
            with open(key_path, "r") as f:
                key = f.read()
                key = RSA.importKey(key)
                key = PKCS1_v1_5.new(key)
            res = []
            with open(soure_file, "rb") as file:
                msg = file.read()
                for i in range(0, len(msg), length):
                    res.append(key.decrypt(msg[i:i + length], 'xyz'))
            with open(decrypt_file, "wb") as file:
                for i in res:
                    file.write(i)
            return True

    # if __name__ == '__main__':
    #     RsaFile.creatKeys()  # 生成kyes 默认名称'public.pem 'private.pem
    #     RsaFile.rsaEncrypt('public.pem', 'a.xlsx')  # public.pem生成的公钥，a.xlsx加密文件,默认加密后文件名Encrypt
    #     RsaFile.rsaDecrypt('private.pem', "Encrypt", "dfc.xlsx")  # private.pem私钥文件,Encrypt需要解密的文件，dfc.xlsx解密后文件


if __name__ == '__main__':
    # getFilePath("./")
    RsaFile.creatKeys()

