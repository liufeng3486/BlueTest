BlueTest
====================

测试工程师使用的标准测试库。包含接口、压力、UI测试相关一站式解决方案

要求
------------
* `Python`_ 3.5.3+
* `Request`_ 2.0.0+

Python下载路径 ``https://www.python.org/downloads/`` 

Request下载路径 ``https://pypi.org/project/requests/``  or 使用pip命令 ``pip install requests``

安装
------------
最简单的安装方式就是使用``pip``命令，作为一个pythoner,``pip``是必备工具之一

.. code-block:: html

    pip install BlueTest 
    pip3 install BlueTest # 双python环境 python3 pip   

**试一下，傻瓜式的Demo**

.. code-block:: python

    >>>import BlueTest
    >>>BlueTest.test()        #接口基础测试DEMO
    >>>BlueTest.presstest()   #接口压测DEMO
    - INFO: 测试数据生成 .//srcdata//test.json.postman_collection
    - INFO: postman转csv成功:./srcdata/test.csv
    - DEBUG: CSV文件内容序列化成功:[{'Lv': '', 'Cname': '', ...
    - INFO: log exceptionCheck: 普通请求 ...
    - INFO: log exceptionCheck: ['date']为空 ...
    - INFO: log exceptionCheck: ['date']不传 ...

-------------------
至此，你已经完成了自动化测试从0-1的壮举。


项目结构
------------

.. code-block:: html

    │  test.py 
    │
    ├─log             
    │      all.log        
    │      error.log
    │
    ├─result
    │      data.txt
    │      Press_1.txt
    │      Press_2.txt
    │      resualt.csv
    │      time.csv
    │
    └─srcdata
            test.csv
            test.json.postman_collection

test.py测试脚本，请自行创建

 ``log`` ， ``result``  ， ``srcdata`` 3个目录由BlueTest自行生成，用户无需关心
  ``log`` 日志文件夹，
  
   * ``all.log`` 全部日志，隔天会自动重建并归档，
   * ``error.log`` 错误日志
 
  ``result`` 执行结果文件夹

  * ``data.txt`` 接口基本测试结果,   
  * ``Press_x.txt`` 压力测试原始数据 ,  
  * ``resualt.csv``  ``time.csv`` 压力测试统计后结果
  
   ``srcdata`` 测试入口数据   

  * ``test.json.postman....`` POSTMAN导出文件 使用BluetTest.test()会自动创建一个demo，正式使用时需要用户自行添加
  * ``test.csv`` 根据 ``test.json.postman....`` 生成的中间文件
 
*PS:之所以使用csv格式为转换和统计压力测试结果，是为了兼容不同的操作系统。而且便于后期的图表生成*

Table of Contents
-----------------
.. toctree::
   Quickstart 
   DetailedSteps
   Demos
   Markup
   methods
   events
   keyboard
   i18n
