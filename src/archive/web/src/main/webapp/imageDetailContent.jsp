<%@ taglib prefix="s" uri="/struts-tags" %>
<%--
  Created by IntelliJ IDEA.
  User: cnlab
  Date: 2015/1/26
  Time: 0:27
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title></title>
    <style type="text/css">
        .img-holder{
            text-align: center;;
        }
        .img-holder img
        {
            box-shadow: 0 3px 3px rgba(0, 0, 0, 0.3);
            border:1px solid #ccc;
            padding:2px;
        }
        .image-des{
            text-align: left;;
        }
        .image-date{
            border-top:1px solid #ccc;
            padding:5px;
        }
    </style>
</head>
<body>
<!-- main -->
<div class="main">
    <!-- shell -->
    <div class="shell">
        <div class="container">
            <div class="img-holder">
                <img src="images/detailImage.jpg">
                <h3><s:property value="singleImage.name" /></h3>
                <p class="image-des"><em>Description:</em><s:property value="singleImage.description" /></p>
            </div>
            <div style="text-align: right"><span class="image-date">[Date: <s:date format="yyyy-MM-dd hh:mm:ss" name="singleImage.createDate" />]</span></div>
            <!-- end of cols -->
        </div>
        <!-- end of shell -->
    </div>
    <!-- end of container -->
</div>
</body>
</html>
