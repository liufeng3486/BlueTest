**目录 (Table of Contents)**

[TOC]


# 简介
:tw-1f317:几个本质懒到家，却被工作压迫的人。为了降低自己的工作量，拍脑袋决定编写一个让小白也可以使用的测试库。一切的出发点都是几个懒人在实际工作中遇到的问题和场景。做这一切的目的是为了少做事。:tw-1f317:
# 功能介绍
## 接口测试
> 参数模板 下文的介绍中会使用该模板进行说明
url = "https://test/api/log?requestID=testid&clientToken=testtoken"
body ={"date": "2018-11-04 10:10:10",
	"actions": [{"actionTime": 1542248466944,"note"]}}

----

### 接口基础校验
----
	参数值判空校验
----
链接中的参数校验,即一般情况下GET参数的校验,以requestID为例:
>url = "https://test/api/log?requestID=&clientToken=testtoken"

请求主体参数的校验，即一般情况下POST参数的校验，form,raw等参数类型均自动处理。
以body中的date为例，请求参数如下:
>body ={"date": "",
	"actions": [{"actionTime": 1542248466944,"note"]}}

以body中的actions[0][actionTime]为例，请求参数如下:
>body ={"date": "2018-11-04 10:10:10",
	"actions": [{"actionTime": "","note"]}}

空值以空字符串为标准。

----
	参数判空校验
----
链接中的参数校验,即一般情况下GET参数的校验,以requestID为例:
>url = "https://test/api/log?clientToken=testtoken"

请求主体参数的校验，即一般情况下POST参数的校验，form,raw等参数类型均自动处理。
以body中的date为例，请求参数如下:
>body ={
	"actions": [{"actionTime": 1542248466944,"note"]}}

以body中的actions[0][actionTime]为例，请求参数如下:
>body ={"date": "2018-11-04 10:10:10",
	"actions": [{"note"]}}

	参数长度校验
----
参数长度校验范围为1-100000。

----


>接口性能测试
待添加
UI自动化
功能已实现，说明待添加

# 安装说明
安装命令`pip install BlueTest`

or

https://pypi.org/project/BlueTest/

# 使用说明及范例

##范例
```python
└─Project
        test1.py
```
test1.py：
```python
import BlueTest
BlueTest.test()
```
---
```python
└─Project
│  test1.py
├─log
│      all.log #日志
│      error.log #错误日志
├─result #结果
│      data.txt
└─srcdata
    │  test.csv  #postman文件的序列化
    │  test.json.postman_collection #范例的postman文件
    └─api #根据postman生成的相关接口py文件
            log.py
```

##使用说明
```python
import BlueTest
BlueTest.initPostMan("test") #执行完成会生成相应csv文件
#默认postamen文件路径.//srcdata//name.json.collection
#默认csv文件生成路径.//srcdata//test.csv
BlueTest.testByCsvData("test") #执行完成会生成相应结果
#结果包括 日志文件log 结果文件resul
```
---
```python
BlueTest.initPostMan("test") #执行完成会生成相应csv文件
BlueTest.initPostMan("test",result_path=path) #指定csv文件生成路径
```

```python
BlueTest.testByCsvData("test") #执行完成会生成相应结果
BlueTest.testByCsvData("test",normal_test=True) #进行接口基础验证
BlueTest.testByCsvData("test",normal_test=Fasle) #不进行接口基础验证
BlueTest.testByCsvData("test",mkpy=True) #生成接口py文件范例如下
```
>import requests
url = "https://nbrecsys.4paradigm.com/action/api/log"
querystring = {'requestID': 'Abac6ban', 'clientToken': '1f9d3d10b0ab404e86c2e61a935d3888'}
payload = {"date":"2018-11-04 10:21:06","actions":[{"requestID":"2222","actionTime":1542248466944,"action":"show","sceneId":420,"userId":"xubyCjC6zO","itemId":"user_define","itemSetId":"39","uuid_tt_dd":"10_28867322960-222-222","specialType":"csdn_net_alliance_ads","ads":1}]}
headers ={'Origin': ' https://blog.csdn.net',
	 'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
	 'Content-Type': ' text/plain',
	 'Accept': ' */*',
	 'Referer': ' https://blog.csdn.net/qq_37159430/article/details/79970518',
	 'Accept-Encoding': ' gzip, deflate, br',
	 'Accept-Language': ' zh-CN,zh;q=0.8'}
response = requests.request("POST", url, params=querystring,data=payload,)
print(response.text)

其他功能详见源码



