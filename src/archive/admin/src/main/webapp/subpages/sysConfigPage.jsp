<%--
  Created by IntelliJ IDEA.
  User: LiuYingBo
  Date: 2015/2/1
  Time: 11:08
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <jsp:include page="headerTemplate.jsp"></jsp:include>
    <style>
        p, h2, ul, li {
            margin: 0px;
            padding: 0px;
        }

        li {
            margin-left: 50px;
        }

        h2 {
            color: white;
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
</head>
<body>
<div title="配置页" style="padding:10px">
    <div style="border:1px solid #ccc;padding:20px;background:#F4F4F4;box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.2);">
        <p style="font-size:14px">配置项目</p>
    </div>
</div>
<script type="text/javascript">
    window.parent.window.ajaxLoadEnd();
    function formatDateTime(val, row) {
        var value;
        try {
            value = new Date(val).toLocaleString();
        } catch (e) {
            value = val;
        }
        return value;
    }

</script>
</body>
</html>
