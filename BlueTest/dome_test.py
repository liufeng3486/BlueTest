null = "null"
# from BlueTest.logInit import *
import BlueTest,time,random

def test():
    with open(".//srcdata//test.json.postman_collection","w") as file:
        a = {
            "id": "3560d742-c3da-4ad7-32c1-222",
            "name": "test",
            "requests": [
                {
                    "id": "49c2b90f-8ea7-c53e-910b-222",
                    "headers": "Origin: https://blog.csdn.net\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\nContent-Type: text/plain\nAccept: */*\nReferer: https://blog.csdn.net/qq_37159430/article/details/79970518\nAccept-Encoding: gzip, deflate, br\nAccept-Language: zh-CN,zh;q=0.8",
                    "url": "https://nbrecsys.4paradigm.com/action/api/log?requestID=Abac6ban&clientToken=1f9d3d10b0ab404e86c2e61a935d3888",
                    "pathVariables": {},
                    "preRequestScript": null,
                    "method": "POST",
                    "collectionId": "3560d742-c3da-4ad7-32c1-222",
                    "data": [],
                    "dataMode": "raw",
                    "name": "testapi",
                    "description": "",
                    "descriptionFormat": "html",
                    "time": 1542777522436,
                    "version": 2,
                    "responses": [],
                    "tests": null,
                    "currentHelper": "normal",
                    "helperAttributes": {},
                    "rawModeData": "{\"date\":\"2018-11-04 10:21:06\",\"actions\":[{\"requestID\":\"2222\",\"actionTime\":1542248466944,\"action\":\"show\",\"sceneId\":420,\"userId\":\"xubyCjC6zO\",\"itemId\":\"user_define\",\"itemSetId\":\"39\",\"uuid_tt_dd\":\"10_28867322960-222-222\",\"specialType\":\"csdn_net_alliance_ads\",\"ads\":1}]}"
                }
            ],
            "order": [
                "49c2b90f-8ea7-c53e-910b-05a3c7014269"
            ],
            "timestamp": 1542777522437
        }
        file.write(str(a))
        BlueTest.log.logger.info("测试数据生成 .//srcdata//test.json.postman_collection")
        # time.sleep(1)
    BlueTest.initPostMan("test")
    BlueTest.testByCsvData("test")
    # BlueTest.testByCsvData("test", limit_check=False, extras_check=True)
def presstest():
    temp = ["temp1", "temp2", "temp3"]
    class press_2(BlueTest.SoloPress):
        def setup(self):
            self.num = temp[0]
            self.count = 20
        def runcase(self):
            response = random.choice(["成功","失败"])
            self.file_write(str(self.num), response, BlueTest.toolbox.responseAssert(response))
    press = BlueTest.Press(2000)
    press.run(press_2)
    press.dataReduction()
def pressTestByCsv():
    a = BlueTest.Csv2Dict(path="./srcdata/test.csv")
    a = a.run()
    b = BlueTest.apiTest(a[0])
    b.error_list = ["error", "Error", "False", "false", "失败", "错误", "异常", "禁止"]
    temp = ["temp1", "temp2", "temp3"]
    class press_2(BlueTest.SoloPress):
        def setup(self):
            self.num = temp[self.index-1]
            self.count = 20

        def runcase(self):
            response = b.soloRequest()
            #dothing ....
            self.file_write(str(self.num),response,b.responseAssert(response))
            # print (self.name,self.num)
    press= BlueTest.Press(2)
    press.run(press_2)
    press.dataReduction()

if __name__ == '__main__':
    pass
    # test()