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
    <title>Introduction</title>
    <jsp:include page="headerPage.jsp"/>
</head>
<body>
<!-- begin of wrapper -->
<div id="wrapper">
    <jsp:include page="menu.jsp"/>
    <div class="main">
        <!-- shell -->
        <div class="shell">
            <div class="container">
                <h3>Introduction</h3>

                <p class="desc">
                    The Chinese Spectral Radioheliograph (CSRH) is a solar-dedicated radio interferometric array that is
                    optimized to carry out imaging spectroscopy of the Sun, to produce high spatial resolution (maximum
                    1.4”), high time resolution (<100ms) and high frequency resolution (about 1%) images of the Sun
                    simultaneously at a wide range of frequencies (Yan et al., 2004). It located in the Inner Mongolia,
                    which is about 400 km away from NAOC.
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