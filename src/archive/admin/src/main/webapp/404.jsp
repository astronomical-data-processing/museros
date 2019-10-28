<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8" isErrorPage="true" %>
<%@ page import="java.io.*,java.util.*" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=US-ASCII">
    <title>Error Page</title>
</head>
<body>
    <%
    response.setStatus(HttpServletResponse.SC_OK);
%>
<body style="text-align:center">
程序发生了错误，有可能该页面正在调试或者是设计上的缺陷.
<br/>
你可以选择
<br/>
<a href=<%=request.getContextPath() + "/forum/new.jsp"%>>反馈</a> 提醒我 或者
<br/>
<a href="javascript:history.go(-1)">返回上一页</a>
<hr width=80%>
<h2>
    <font color=#DB1260>JSP Error Page</font>
</h2>

<p>
    An exception was thrown:
    <b><%=exception.getClass()%>:<%=exception.getMessage()%>
    </b>
</p>
<%
    Enumeration<String> e = request.getHeaderNames();
    String key;
    while (e.hasMoreElements()) {
        key = e.nextElement();
    }
    e = request.getAttributeNames();
    while (e.hasMoreElements()) {
        key = e.nextElement();
    }
    e = request.getParameterNames();
    while (e.hasMoreElements()) {
        key = e.nextElement();
    }
%>
<%=request.getAttribute("javax.servlet.forward.request_uri")%>
<br>
<%=request.getAttribute("javax.servlet.forward.servlet_path")%>
<p>
    With the following stack trace:
</p>
 <pre>
 <%
     exception.printStackTrace();
     ByteArrayOutputStream ostr = new ByteArrayOutputStream();
     exception.printStackTrace(new PrintStream(ostr));

 %>
</pre>
<hr width=80%>
</body>
</html>