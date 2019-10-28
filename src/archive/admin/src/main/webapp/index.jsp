<%@ page import="java.util.List" %>
<%@ page import="java.util.ArrayList" %>
<%@ page import="org.cnlab.common.MenuItemModel" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="s" uri="/struts-tags" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/metro-orange/easyui.css">
    <link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/icon.css">
    <link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/color.css">
    <script type="text/javascript" src="lib/jquery-easyui-1.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="lib/jquery-easyui-1.4.1/jquery.easyui.min.js"></script>
    <script type="text/javascript" src="lib/jquery-easyui-1.4.1/locale/easyui-lang-zh_CN.js"></script>
    <style>
        * {
            font-family: "Microsoft YaHei" ! important;
        }

        html, body {
            border: none;
            font-family: "Microsoft YaHei" ! important;
            overflow: hidden;
        }

        p, h2 {
            margin: 0px;
            padding: 0px;
        }

        h2 {
            color: white;
        }

        .btnMenu {
            width: 100%;
            height: 50px;
        }

        #shortbar a {
            color: white;
            text-decoration: none;
            padding: 1px 5px 0px 5px;
        }

        #shortbar a:hover {
            text-decoration: underline;
        }
    </style>
    <script type="text/javascript">
        /*遮罩层开始B-这里放在主页上面*/
        function ajaxLoadBegin(){
            $("<div class=\"datagrid-mask\"></div>").css({display:"block",width:"100%",height:$(window).height()}).appendTo("body");
            $("<div class=\"datagrid-mask-msg\" style=\"font-size:12px;\"></div>").html("正在处理，请稍候。。。").appendTo("body").css({display:"block",left:($(document.body).outerWidth(true) - 190) / 2,top:($(window).height() - 45) / 2});
        }
        /*遮罩层结束B-在子页面<iframe>里面要调用window.parent.window.ajaxLoadEnd();来关闭*/
        function ajaxLoadEnd(){
            try{
                $(".datagrid-mask").remove();
                $(".datagrid-mask-msg").remove();
            }catch(e)
            {
                //如果到这里说明不存在遮罩，可能由于操作导致
                alert("前台操作异常，请联系管理员！");
            }
        }
        function createFrame(url) {
            var s = '<iframe scrolling="auto" frameborder="0"  src="' + url + '" style="width:100%;height:100%;"></iframe>';
            return s;
        }
        function openTab(target, url) {
            var buttonId = target.id;
            var title = $("#" + buttonId).linkbutton().text();
            if (buttonId && title) {
                if (!$('#contentPanel').tabs('exists', title)) {
                    ajaxLoadBegin();
                    $('#contentPanel').tabs('add', {
                        title: title,
                        content: createFrame(url),
                        closable: true
                    });
                } else {
                    $('#contentPanel').tabs('select', title);
                }
            }
        }
    </script>
</head>
<body style="padding:0px;margin:0px;">

<div class="easyui-layout" style="width:100%;height:100%;" data-options="fit:true">
    <div data-options="region:'north'" style="height:50px;border:none;">
        <div class="easyui-layout" style="width:100%;height:100%;" ;>
            <div data-options="region:'west'" style="width:400px;background: #DE8033;overflow:hidden;border: none;">
                <div style="overflow:hidden;padding-left:10px;color:white;">
                    <img src="images/logo.png" alt="MUSER数据管理系统"/>
                </div>
            </div>
            <div data-options="region:'center'" style="width:100%;background: #DE8033;border: none;"></div>
            <div data-options="region:'east'" style="width:300px;background: #DE8033;border: none;">
                <div style="text-align:right;padding:5px 10px 0 25px;color:white;" id="shortbar"><a href="#">帮助</a>|<a
                        href="#">建议</a>|<a href="login/login_toLogout.action">退出</a>
                </div>
            </div>
        </div>
    </div>
    <div data-options="region:'west'" style="width:75px;background: #DE8033;overflow:hidden;border:none;">
        <s:iterator value="#session.menuList" var="menu">
        <p>
            <a href="#" class="easyui-linkbutton btnMenu"
               data-options="iconCls:'<s:property value="#menu.icon"/>',iconAlign:'top'"  id="<s:property value='#menu.id'/>"
               onclick="openTab(this,'<s:property value='#menu.url'/>')"><s:property value="#menu.name"/>
            </a>
        <p>
        </s:iterator>
    </div>
    <div data-options="region:'center'" style="border:none;">
        <div class="easyui-tabs" id="contentPanel" style="width:100%;height:100%">
        </div>
    </div>
</div>
</div>
<script type="text/javascript">
    $(function () {
        $("#mgrHomePage").click();
        $('#contentPanel').tabs({
            border:false,
            onSelect: function (title) {
                var currTab = $('#contentPanel').tabs('getTab', title);
                var iframe = $(currTab.panel('options').content);
                var src = iframe.attr('src');
                if (src)
                    $('#contentPanel').tabs('update', {
                        tab: currTab,
                        options: {
                            content: createFrame(src)
                        }
                    });
            }
        });
    });
</script>
</body>
</html>
