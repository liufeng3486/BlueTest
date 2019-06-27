HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://pypi.org/static/css/warehouse.d8da1ae4.css">
    <link rel="stylesheet" href="https://pypi.org/static/css/fontawesome.3173d2f0.css">
    <link rel="stylesheet" href="https://pypi.org/static/css/regular.19624371.css">
    <link rel="stylesheet" href="https://pypi.org/static/css/solid.f478cfb1.css">
    <link rel="stylesheet" href="https://pypi.org/static/css/brands.1ea560bf.css">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>

    %(stylesheet)s

    <script language="javascript" type="text/javascript">
output_list = Array();

/*level 调整增加只显示通过用例的分类 --Findyou
0:Summary //all hiddenRow
1:Failed  //pt hiddenRow, ft none
2:Pass    //pt none, ft hiddenRow
3:All     //pt none, ft none
*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }

    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}

function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}

function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
</head>
<body data-controller="viewport-toggle" style="padding-top: 0px;">
    <header class="site-header ">
        <div class="site-container">
            <div class="split-layout">
                <div data-html-include="/_includes/current-user-indicator/">
                    <nav id="user-indicator" class="horizontal-menu horizontal-menu--light horizontal-menu--tall" aria-label="Main navigation">
                        <a class="horizontal-menu__link horizontal-menu__link--remove-on-mobile" >测试报告</a>
                        <a class="horizontal-menu__link horizontal-menu__link--remove-on-mobile" href="/help/">预留</a>
                        <a class="horizontal-menu__link horizontal-menu__link--remove-on-mobile" href="/help/">预留</a>
                    </nav>
                </div>
            </div>
          </div>
    </header>
    <main id = "content">
        <section data-controller="project-tabs" data-project-tabs-content="description">
            <div class="tabs-container">
                <div class="vertical-tabs">
                    <div class = "vertical-tabs__tabs">
                        <div class="sidebar-section">
                            <h3 class="sidebar-section__title">常规</h3>
                            <nav role="tablist">
                              <a id="description-tab" class="vertical-tabs__tab "  role="tab">
                                测试人员 : %(tester)s
                              </a>
                              <a id="description-tab" class="vertical-tabs__tab "  role="tab">
                                开始时间 : %(startTime)s
                              </a>
                              <a id="description-tab" class="vertical-tabs__tab "  role="tab">
                                合计耗时 : %(userTime)s
                              </a>
                            </nav>
                        </div>

                        <div class="sidebar-section">
                            <h3 class="sidebar-section__title">结果</h3>
                            <a class="btn btn-primary" href='javascript:showCase(0)'>概要 %(passrate)s </a><br/><br/>
<a class="btn btn-danger" href='javascript:showCase(1)'>失败 %(fail)s </a><br/><br/>
<a class="btn btn-success" href='javascript:showCase(2)'>通过 %(Pass)s </a><br/><br/>
<a class="btn btn-info" href='javascript:showCase(3)'>所有 %(count)s </a>


                        </div>
                        <div class="sidebar-section">
                            <h3 class="sidebar-section__title">其他</h3>
                                    <p>本报告站点服务由服务中心提供,用于支持由<a href="http:">XXXX</a>生产的测试报告预览，管理员为<a href="http:">XXXX</a></p>
                                </div>

                    </div>

                    <div class = "vertical-tabs__panel">

                        %(report)s
                        %(ending)s
                    </div>
</body>
</html>
"""

STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }

/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>
"""

HEADING_TMPL = """<div class='heading'>
<h1 style="font-family: Microsoft YaHei">%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>

"""

HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
"""

REPORT_TMPL = """
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>错误</td>
    <td>详细</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>通过率：%(passrate)s</td>
</tr>
</table>
"""

REPORT_CLASS_TMPL = r"""
<tr class='%(style)s warning'>
    <td>%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
    <td class="text-center">%(error)s</td>
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
</tr>
"""

REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>
    <!--默认收起错误信息 -Findyou
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse">  -->

    <!-- 默认展开错误信息 -Findyou -->
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs " data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse in">
    <pre>
    %(script)s
    </pre>
    </div>
    </td>
</tr>
"""

REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>
    <!--默认展开错误信息 -Findyou
    <button id='btn_%(tid)s' type="button"  class="btn btn-success btn-xs " data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse">  -->

    <!-- 默认收起错误信息 -Findyou -->
    <button id='btn_%(tid)s' type="button"  class="btn btn-success btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse">
    <pre>
    %(script)s
    </pre>
    </div>
    </td>
</tr>
"""

REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
"""

ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """