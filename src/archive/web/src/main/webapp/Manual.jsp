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
    <title>Manual</title>
    <jsp:include page="headerPage.jsp"/>
</head>
<style type="text/css">
    .item-area-header, .item-area-body {
        padding: 20px 20px 0px 20px;;
    }

    .item-area-header {
        font-weight: bold;
        font-size: 14px;
    }

    .item-area-body ul {
        margin-left: 50px;
    }
</style>
<body>
<!-- begin of wrapper -->
<div id="wrapper">
    <jsp:include page="menu.jsp"/>
    <div class="main">
        <!-- shell -->
        <div class="shell">
            <div class="container">
                <h3>Softwares and Manual</h3>

                <p class="desc">

                <div class="item-area">
                    <div class="item-area-header">Analysis Manual</div>
                    <div class="item-area-body">
                        <ul>
                            <li><a href="doc/manual/index.html">
                                <strong>Japanese</strong></a>
                                (<a href="doc/manual/index.html">HTML</a>,
                                <a href="doc/manual.tex">LaTex</a>,
                                <a href="doc/manual.pdf">PDF</a>)


                            </li>
                            <li><a href="doc/manuale/index.html">
                                <strong>English</strong></a>
                                (<a href="doc/manuale/index.html">HTML</a>,
                                <a href="doc/manuale.tex">LaTex</a>,
                                <a href="doc/manuale.pdf">PDF</a>)
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="item-area">
                    <div class="item-area-header">Databook</div>
                    <div class="item-area-body">
                        <ul>
                            <li>Volume 1 (1992 Jun - 1994 Dec)
                            </li>
                            <li>Volume 2 (1995 Jan - 1997 Dec)
                            </li>
                            <li><a href="doc/databook_vol3/">Volume 3</a> (1998 Jan - 2000 Dec)
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="item-area">
                    <div class="item-area-header"> Softwares & Data Base</div>
                    <div class="item-area-body">
                        <ul>
                            <li><a href="soft">
                                <strong>Softwares</strong></a>
                                <ul>
                                    <li><a href="idl">
                                        <strong>IDL package</strong></a>
                                    </li>
                                    <li><a href="soft/synthesis">
                                        <strong>Synthesis programs</strong></a>
                                        <ul>
                                            <li><a href="soft/synthesis/hanaoka">
                                                <strong>Hanaoka</strong></a><br>
                                                Standard CLEAN algorithm.
                                                Support 17/34GHz, Full/Partial Sun images.
                                                Run on Sun/Sparc, NEC/SX, NEC/EWS.
                                            </li>
                                            <li><a href="soft/synthesis/koshix">
                                                <strong>Koshix</strong></a><br>
                                                CLEAN + Steer algorithm. Better for
                                                diffuse radio sources.
                                                Support 17GHz, Full/Partial Sun images.
                                                Run on Sun/Sparc, NEC/SX, NEC/EWS.
                                            </li>
                                        </ul>
                                    </li>
                                    <li><a href="soft/utility">
                                        <strong>Utility</strong></a>
                                    </li>
                                    <li><a href="soft/c2fits">
                                        <strong>C2FITS</strong></a><br>
                                        This program is for reconstructing the
                                        NoRH raw data to visivility data that can be utilized
                                        for AIPS synthesizing software.
                                    </li>
                                    <li><a href="soft/helioglib">
                                        <strong>HeliogLib</strong></a><br>
                                        This Fortran library contains subroutines for IO interface
                                        to the NoRH raw data and synthesizing algorithms.
                                    </li>
                                </ul>
                            </li>
                            <li><a href="data">
                                <strong>Data Base</strong></a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="item-area">
                    <div class="item-area-header">Image FITS</div>
                    <div class="item-area-body">
                        <ul>
                            <li><a href="images/daily">
                                <strong>Daily Image FITS</strong></a>
                            </li>
                            <li><a href="images/event">
                                <strong>Event Image FITS</strong></a>
                            </li>
                            <li><a href="images/10min">
                                <strong>10min FITS</strong></a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div class="item-area">
                    <div class="item-area-header">FTP Server</div>
                    <div class="item-area-body">
                        <ul>
                            <li><a href="#">
                                <strong>Raw Data</strong></a>
                            </li>
                            <li><a href="#">
                                <strong>WWW server</strong></a>
                            </li>
                            <li><a href="#">
                                <strong>FTP server</strong></a>
                            </li>
                        </ul>
                    </div>
                </div>
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