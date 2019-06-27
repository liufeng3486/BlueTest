class td():
    def id(self):
        return "__main__.MyTestCase.testCase1"
    def shortDescription(self):
        return "shortDescription"
class Test():
    def id(self):
        return "Test1"+".test1"

    def shortDescription(self):
        return "shortDescription"
class Test2():
    def id(self):
        return "Test2"+".test1"

    def shortDescription(self):
        return "shortDescription"
class Report():
    def __init__(self):
        self.result=[]
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.tester = "Temp"
        self.start_time = ""
        self.use_time = ""
        self.passrate = float(0)

    def Arrangement(self):
        for solo in self.result:
            if solo[0] == 0:
                self.success_count += 1
            elif solo[0] == 1:
                self.failure_count += 1
            else:
                self.error_count += 1
    def Result(self):
        dd = Test()
        ff = Test2()
        self.result =  [(1,dd,"错误的说明","备注"),(1, dd, "错误的说明", "备注")
            , (0, dd, "", "备注"),(1,ff,"错误的说明","备注"),(1, ff, "错误的说明", "备注")
            , (0, ff, "", "备注")]
    def getReportAttributes(self):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        # startTime = str(self.startTime)[:19]
        # duration = str(self.stopTime - self.startTime)
        status = []
        status.append('共 %s' % (self.success_count + self.failure_count + self.error_count))
        if self.success_count: status.append('通过 %s'    % self.success_count)
        if self.failure_count: status.append('失败 %s' % self.failure_count)
        if self.error_count:   status.append('错误 %s'   % self.error_count  )
        if status:
            status = '，'.join(status)
            self.passrate = str("%.2f%%" % (float(self.success_count) / float(self.success_count + self.failure_count + self.error_count) * 100))
        else:
            status = 'none'
        return [
            ('测试人员', self.tester),
            ('开始时间',self.start_time),
            ('合计耗时',self.use_time),
            ('测试结果',status + "，通过率= "+self.passrate),
        ]

