
#report的demo 未完善
import BlueTest

import random

class Resualt():
    def __init__(self):
        self.__class__.__name__ = "123123"
        self.result = 2
    def id(self):
        return ""+".test1"
    def shortDescription(self):
        return "shortDescription"

class Test():
    def __init__(self):
        self.results = []
    def solorun(self):
        self.i += 1
        dd = Resualt()
        return (random.randint(0,1),dd,"error message","ps")
    def run(self):
        self.i = 1
        for i in range(5):
            self.results.append(self.solorun())
    def Result(self):
        self.run()
        return self.results


if __name__ == '__main__':
    runner = BlueTest.HTMLTestRunner(
        stream='D:\\HTMLTestReportCN4.html',
        title='title222',
        description='',
        tester='tester'
        )
    #运行测试用例
    d = BlueTest.Report()
    d.Result()
    d.result = Test().Result()
    d.Arrangement()
    runner.run(d)
    # 关闭文件，否则会无法生成文件
    #fp.close()