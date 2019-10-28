<%@ taglib prefix="s" uri="/struts-tags" %>
<%--
  Created by IntelliJ IDEA.
  User: cnlab
  Date: 2015/1/26
  Time: 0:25
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title></title>
</head>
<body>
<!-- header -->
<header id="header">
    <!-- shell -->
    <div class="shell">
        <div class="header-inner">
            <!-- header-cnt -->
            <div class="header-cnt">
                <h1 id="logo"><a href="#">Simple</a></h1>

                <p>
                    <span class="mobile">The Mingantu Ultrawide SpEctral Radioheliograph (MUSER) is a synthetic aperture radio interferometer built in Mingantu town, Inner Mongolia of China. As a solar-dedicated interferometric array, the MUSER can produce high quality radio images in a frequency range of 400 MHz - 15 GHz with high temporal, spatial, and spectral resolution.</span>
                </p>
            </div>
            <!-- end of header-cnt -->
            <!-- slider -->
            <div class="slider-holder">
                <div class="flexslider">
                    <ul class="slides">
                        <li><img src="images/slide-img.png" alt=""/></li>

                        <li><img src="images/t1.jpg" alt=""/></li>

                        <li><img src="images/t2.jpg" alt=""/></li>

                        <li><img src="images/t3.jpg" alt=""/></li>

                        <li><img src="images/t4.jpg" alt=""/></li>
                    </ul>
                </div>
            </div>
            <!-- end of slider -->
            <div class="cl">&nbsp;</div>
        </div>
        <div class="cl">&nbsp;</div>
    </div>
    <!-- end of shell -->
</header>
<!-- end of header -->
<!-- main -->
<div class="main">
    <span class="shadow-top"></span>
    <!-- shell -->
    <div class="shell">
        <div class="container">
            <section class="blog">
                <!-- content -->
                <div class="content">
                    <div class="cnt">
                        <h3>MUSER Introducton</h3>

                        <p>MUSER is an interferometer under construction in China. The MUSER will consist of 100
                            telescopes covering 0.4–15 GHz. 40 telescopes of 4.5 m cover 400 MHz-2 GHz and 60 telescopes
                            of 2 m cover 2–15 GHz. CSRH will be one of the world’s largest and most advanced imaging
                            spectroscopy instruments. CSRH will be used to study coronal mass ejections. All of the 4.5m
                            telescopes are assembled and the 2m telescopes will be assembled by 2013.</p>
                        <ul>
                            <li><a href="Intro.jsp">Introduction</a></li>
                            <li><a href="Policy.jsp">Data Use Policy</a></li>
                            <li><a href="Results.jsp">Gallery, Major Results </a></li>
                            <li><a href="Manual.jsp">Archive, Softwares, and Manuals</a></li>
                        </ul>
                    </div>
                </div>
                <!-- end of content -->

                <!-- sidebar -->
                <aside class="sidebar">
                    <!-- widget -->
                    <div class="widget">
                        <h3>Latest CLEAN Images</h3>
                        <ul>
                            <s:iterator value="part.imageList" status="statu">
                                <li>
                                    <div class="img-holder">
                                        <a href="javascript:void(0)"><img src="images/post-img.png"
                                                                          alt="<s:property value="name" />"/></a>
                                    </div>

                                    <p>
                                        <a href="image_detail.action?token=XDSDEWRSXDFASDF&imageID=<s:property value="imageID" />"><s:property
                                                value="description"/>
                                        </a><span><s:date format="yyyy-MM-dd hh:mm:ss" name="createDate"/></span></a>
                                    </p>
                                </li>
                            </s:iterator>
                        </ul>
                        <div class="cl">&nbsp;</div>
                    </div>
                    <!-- end of widget -->
                </aside>
                <!-- end of sidebar -->
                <div class="cl">&nbsp;</div>
            </section>
            <div class="shadow-bottom"></div>
            <!-- cols -->
            <section class="cols">
                <div class="col">
                    <h3>Tools & Libs Used in MUSER</h3>
                    <img src="images/cols-img.png" alt="" class="alignleft"/>

                    <div class="col-cnt">
                        <p>
                            <a href="ftp://test:gsdjsj@222.197.221.231/2014">Tools</a>
                        </p>

                        <p>
                            <a href="ftp://test:gsdjsj@222.197.221.231/2014">Softwares and Libs</a>
                        </p>

                        <p>
                            <a href="ftp://test:gsdjsj@222.197.221.231/2014">Radio Interferometer </a>
                        </p>
                    </div>
                </div>
                <div class="col">
                    <h3>Study & Meetings in MUSER</h3>
                    <img src="images/cols-img2.png" alt="" class="alignleft"/>

                    <div class="col-cnt">
                        <ul>
                            <li><a href="#">Bibliography</a></li>
                            <li><a href="HowTo.jsp">How to Study in MUSER Group </a></li>
                            <li><a href="Meeting.jsp">Meetings organized by MUSER group</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col">
                    <h3>WWW & FTP Servers</h3>
                    <img src="images/cols-img3.png" alt="" class="alignleft"/>

                    <div class="col-cnt">
                        <p>
                            <a href="ftp://test:gsdjsj@222.197.221.231/2014">Raw Data</a>
                        </p>

                        <p>
                            <a href="ftp://test:gsdjsj@222.197.221.231/2014">Clean Images</a>
                        </p>

                        <p>
                            <a href="ftp://test:gsdjsj@222.197.221.231/2014">Movies</a>
                        </p>
                    </div>
                </div>
                <div class="cl">&nbsp;</div>
            </section>
            <!-- end of cols -->
        </div>
        <!-- end of shell -->
    </div>
    <!-- end of container -->
</div>
<!-- end of main -->
</body>
</html>
