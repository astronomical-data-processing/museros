<%--
  Created by IntelliJ IDEA.
  User: cnlab
  Date: 2015/1/26
  Time: 0:15
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title></title>
</head>
<body>
<!-- top-nav -->
<nav class="top-nav">
    <div class="shell">
        <a href="#" class="nav-btn">HOMEPAGE<span></span></a>
        <span class="top-nav-shadow"></span>
        <ul id="menu-wrapper">
            <li class="active" id="menuIndex"><span><a href="index_home.action?linkName=menuIndex">home</a></span></li>
            <li id="menuImage"><span><a href="index_image.action?linkName=menuImage">images</a></span></li>
            <li id="menuMovie"><span><a href="index_movie.action?linkName=menuMovie">movies</a></span></li>
            <li id="menuEvent"><span><a href="index_event.action?linkName=menuEvent">events</a></span></li>
            <li id="menuResearch"><span><a href="index_research.action?linkName=menuResearch">research</a></span></li>
            <li id="menuData"><span><a href="index_data.action?linkName=menuData">data</a></span></li>
            <li id="menuAbout"><span><a href="index_about.action?linkName=menuAbout">about</a></span></li>
        </ul>
    </div>
</nav>
<!-- end of top-nav -->
<script type="application/javascript">
    function getQueryString(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    }
    var activeMenu = $("#menu-wrapper li[class='active']");
    var activeName = getQueryString("linkName");
    var willActiveMenu;
    if (activeName) {
        willActiveMenu = $("#" + activeName);
    }
    if (activeMenu) {
        activeMenu.removeClass("active");
        if (willActiveMenu) {
            willActiveMenu.addClass("active");
        }
    }
</script>
</body>
</html>
