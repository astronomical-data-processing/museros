<%--
  Created by IntelliJ IDEA.
  User: cnlab
  Date: 2015/1/26
  Time: 0:27
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
<link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/metro-orange/easyui.css">
<link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/icon.css">
<link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/color.css">
<script type="text/javascript" src="lib/jquery-easyui-1.4.1/jquery.min.js"></script>
<script type="text/javascript" src="lib/jquery-easyui-1.4.1/jquery.easyui.min.js"></script>
<style type="text/css">
    body {
        font-size: 12px;
        line-height: 22px;
        font-family: arial, sans-serif;
        color: #828282;
        background: url(images/body.png) repeat 0 0;
        min-width: 980px;
    }

    * {
        margin: 0;
        padding: 0;
        outline: 0;
    }

    #content {
        width: 980px;
        margin: 10px auto;
    }

    .seperater {
        height: 25px;
    }
</style>
<script type="text/javascript">
    $(document).ready(function () {
        function formatDateTime(val, row) {
            var value;
            try {
                value = new Date(val).toLocaleString();
            } catch (e) {
                value = val;
            }
            return value;
        };
    });
</script>

<!-- main -->
<div class="main">
    <!-- shell -->
    <div class="shell">
        <div class="container">
            <h1>Chinese Spectral Radioheliograph Event List</h1>

            <div class="seperater"></div>
            <div>Note,EID=EventID,DE=Date,PK=Peak(UT),DN=Duratn(sec),COR=Cor
                (x1.e-4),BN=Brightness(K),F17G=F17G(SFU),F17G=F34G(SFU),AR=Area
                Ratio,PO=Position,X=X("),Y=Y("),IE=#implulse,GOES,NK= NOAA Keyword,RE=RHESSI Energy(keV)
            </div>
            <table id="dg" title="2013 Solar Event" class="easyui-datagrid"
                   url="solarEvent_query.action?"
                   pagination="true"
                   pageList="[30,50,100]"
                   pageSize="30"
                   rownumbers="true" fitColumns="true" singleSelect="true">
                <thead>
                <tr>
                    <th field="eventID" width="20">EventID</th>
                    <th field="date" width="20">Date</th>
                    <th field="peak" width="20">Peak</th>
                    <th field="duratn" width="20">Duratn</th>
                    <th field="cOR" width="20">COR</th>
                    <th field="brightness" width="20">Brightness</th>
                    <th field="f17G" width="20">F17G</th>
                    <th field="f34G" width="20">F34G</th>
                    <th field="areaRatio" width="20">AreaRatio</th>
                    <th field="position" width="20">Position</th>
                    <th field="x" width="20">X</th>
                    <th field="y" width="20">Y</th>
                    <th field="implulse" width="20">Implulse</th>
                    <th field="gOES" width="20">GOES</th>
                    <th field="nOAAKeyword" width="20">NOAA</th>
                    <th field="keyword" width="20">Keyword</th>
                    <th field="rHESSI" width="20">RHESSI</th>
                    <th field="energy" width="20">Energy</th>
                </tr>
                </thead>
            </table>
        </div>
    </div>
</div>
</body>
</html>