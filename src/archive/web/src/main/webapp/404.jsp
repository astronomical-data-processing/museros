<%--
  Created by IntelliJ IDEA.
  User: cnlab
  Date: 2015/2/4
  Time: 14:29
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Error 404 Page</title>
<style type="text/css">
    BODY {
        height: 100%;
        margin: 0;
        overflow: hidden;
        padding: 0;
        width: 100%;
    }
    .msg_tip_body {
        background-color: #fffbe2;
        border: 1px solid #edddab;
        margin: 50px auto;
        min-height: 230px;
        padding-top: 50px;
        width: 950px;
    }
    DIV {
        font-size: 12px;
    }
    .msg_tip_box {
        margin: 0 auto;
        width: 600px;
    }
    DIV {
        font-size: 12px;
    }
    .msg_tip_title {
        border-bottom: 1px solid #6ab3d7;
        height: 25px;
    }
    DIV {
        font-size: 12px;
    }
    .msg_tip_title em {
        color: #163463;
        font-size: 14px;
        font-style: normal;
        font-weight: 700;
        padding-left: 1em;
    }
    .alert_error {
        background: url("images/error_big.gif") no-repeat scroll 0 10px rgba(0, 0, 0, 0);
        margin: 20px;
        padding: 0 0 0 58px;
    }
    DIV {
        font-size: 12px;
    }
    .msg_tip_content {
        color: #fb6c03;
        font: 16px/28px "黑体";
        height: 48px;
    }
    .alert_bl {
        font-size: 14px;
        margin-top: 5px;
    }
    .alert_bl a:link, .alert_bl a:visited {
        color: #29548e;
        text-decoration: underline;
    }
    A {
        color: #1e5494;
    }
</style>
</head>
<body>
<div class="msg_tip_body">
    <div class="msg_tip_box">
        <div class="msg_tip_title">
            <em>
                MUSER-Info
            </em>
        </div>
        <div class="alert_error">
            <p class="msg_tip_content">Sorry, Page can not be found！</p>

            <p class="alert_bl"><a href="javascript:history.go(-1)">back</a></p>
        </div>
    </div>
</div>


</body>
</html>
