<%--
  Created by IntelliJ IDEA.
  User: cnlab
  Date: 2015/1/24
  Time: 12:54
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Result</title>
    <jsp:include page="headerPage.jsp"/>
    <style type="text/css">
        p {
            padding-left: 20px;
        }
    </style>
</head>
<body>
<!-- begin of wrapper -->
<div id="wrapper">
    <jsp:include page="menu.jsp"/>
    <div class="main">
        <!-- shell -->
        <div class="shell">
            <div class="container">
                <h3>MUSER Results</h3>

                <p class="desc">
                    <a href="#"> Daily Observation</a><br>
                    <a href="#"> 1 GK Sun</a><br>
                    <a href="#"> 1 MK Sun</a><br>
                    <a href="#"> 10,000 K Sun</a><br>
                    <a href="#"> Sun Observed at Dual Frequencies</a><br>
                    <a href="#"> Observation with High Temporal Resolution</a><br>
                    <a href="#"> Flare Observed with Various Instruments</a><br>
                    <a href="#"> Eclipse Observed by Radio</a><br>
                    <a href="#"> Transit of Venus in Microwave</a><br>

                </p>
            </div>
            <!-- end of cols -->
        </div>
        <!-- end of shell -->
    </div>
</div>
<!-- end of wrapper -->
<jsp:include page="footer.jsp"/>
</body>
</html>