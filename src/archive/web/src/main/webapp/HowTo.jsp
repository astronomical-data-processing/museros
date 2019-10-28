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
    <title>Howto</title>
    <jsp:include page="headerPage.jsp"/>
    <style type="text/css">
        p {
            padding-left: 20px;
        }

        ul {
            list-style: none;
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
                <h3>Howto</h3>

                <p class="desc">
                <ul>
                    <li><b> How to a User-Account for the NRO/Solar network computers</b>

                        <p>

                            We will give a <font color="red">temporal user ID</font>
                            on our computer system in MUSER/Solar to anybody
                            who wants to study the astronomical/solar plasma physics by using
                            MUSER data (Radioheliograph, Radio Polarimeter). Detailed information
                            is <a href="../computer/">here</a>.
                        </p>

                        <p>

                        </p></li>
                </ul>

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