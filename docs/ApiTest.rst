ApiTest
=======
接口测试，是这个测试脚手架被搭建的初衷。所以代码的没有做到小而美。
秉承着一贯的原则，还是先看我们的范例吧

范例
------
**接口基础测试**

``postman_collection``  测试数据放置于 ``./srcdata/``   目录中

.. code-block:: python

    >>>import BlueTest
        # xxx为测试文件test.json.postman_collection 名称。BlueTest.initPostMan("test")
        # 初始化PostMan测试数据
    >>>BlueTest.initPostMan("test")  #test.json.postman_collection->test.csv
    >>> - INFO: postman转csv成功:./srcdata/test.csv
        #依赖test.csv执行接口测试
    >>>BlueTest.testByCsvData("test")   
    >>> - DEBUG: CSV文件内容序列化成功:[{'Lv': '', 'Cname': '', ...
    >>> - INFO: log exceptionCheck: 普通请求 ...
    >>> - INFO: log exceptionCheck: ['date']为空 ...
    >>> - INFO: log exceptionCheck: ['date']不传 ...
    >>> - INFO: log extrasCheck: ['date'] 额外参数校验 ...
    
**接口压力测试Demo1**

.. code-block:: python

    import BlueTest,random
    class pressTest(BlueTest.SoloPress): #继承压力测试基类BlueTest.SoloPress
        def setup(self):
            self.count = 单线程执行数
        def runcase(self): #重写runcase方法
            response = random.choice(["成功","失败"]) #设置模拟测试数据
            self.file_write(self.name, response, BlueTest.toolbox.responseAssert(response)) #结果记录
    press = BlueTest.Press(线程数) 
    press.run(pressTest)  #执行测试
    press.dataReduction() #统计、整理测试结果
    >>> index:1, run:10% ,num:2
    >>> index:2, run:10% ,num:2
    >>>  ...

**接口压力测试Demo2**

区别于Demo1的地方在于这个例子使用到了由 ``postman->csv`` 的文件。将压力测试与接口测试的数据耦合到一起，可以实现统一管理。

.. code-block:: python

    csv2dict = BlueTest.Csv2Dict(path="./srcdata/test.csv") #加载测试数据 需要填入完整相对/绝对路径
    csv_data = csv2dict.run()  #生成测试数据
    apitest = BlueTest.apiTest(csv_data[0]) #实例化测试单体
    class solopress(BlueTest.SoloPress): 
        def setup(self):
            self.count = 单线程执行数
        def runcase(self):
            response = apitest.soloRequest() 
            self.file_write(str(self.num),response,apitest.responseAssert(response))
    press= BlueTest.Press(线程数)
    press.run(solopress)
    press.dataReduction()

*PS:更多使用方法详见函数说明*


