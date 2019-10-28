<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
    <head>
		<title>MUSER数据发布管理系统登录</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <link rel="stylesheet" type="text/css" href="css/style.css" />
		<style type="text/css">
			html, body {
				border: none;
				overflow: hidden;
				font-size:12px;
			}
			.form_wrapper .bottom,.form_wrapper h3{
				background: #DE8033;
			}
		</style>

    </head>
    <body>
		<div class="wrapper">
			<h1><span style="color:#DE8033">MUSER数据发布管理系统</span></h1>
			<h2>The <span style="color:#DE8033">M</span>ingantu <span style="color:#DE8033">U</span>ltrawide <span style="color:#DE8033">S</span>p<span style="color:#DE8033">E</span>ctral <span style="color:#DE8033">R</span>adioheliograph-MUSER</h2>
			<div class="content">
				<div id="form_wrapper" class="form_wrapper">
					<form class="login active" id="loginForm">
						<h3>管理登录</h3>
						<div>
							<label>用户名:</label>
							<div class="inputWraper">
								<input class="easyui-textbox" validType="length[5,20]" type="text" name="TxtUserName" id="TxtUserName" value="admin" style="width:250px;height:35px;" data-options="required:true">
							</div>
						</div>
						<div>
							<label>密码: </label>
							<div class="inputWraper">
								<input class="easyui-textbox" validType="length[1,20]"  type="password" name="TxtPassword" id="TxtPassword" style="width:250px;height:35px;" value="888888" data-options="required:true">
							</div>
						</div>
						<div class="bottom">
							<div class="loginArea" id="statusBar">
								<input type="checkbox" />
								<span id="status">保持登录状态</span>
								<a href="javascript:void(0)" id="btnLogin" class="easyui-linkbutton c1" style="width:150px;height:45px;font-size: 16px;" onclick='loginFun();'>登录</a>
							</div>
							<div id="tips">提示：注意大小写。</div>
							</div>
					</form>
				</div>
				<div class="clear"></div>
			</div>
		</div>

		<!-- The JavaScript -->
		<!-- JQuery UI. -->
		<link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/metro-orange/easyui.css">
		<link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/icon.css">
		<link rel="stylesheet" type="text/css" href="lib/jquery-easyui-1.4.1/themes/color.css">
		<script type="text/javascript" src="lib/jquery-easyui-1.4.1/jquery.min.js"></script>
		<script type="text/javascript" src="lib/jquery-easyui-1.4.1/jquery.easyui.min.js"></script>
		<script type="text/javascript" src="lib/jquery-easyui-1.4.1/locale/easyui-lang-zh_CN.js"></script>
		<script type="text/javascript" src="lib/jquery-md5/jquery.md5.js"></script>
		<script type="text/javascript" src="lib/jquery-validation-1.13.1/jquery.validate.min.js"></script>
    </body>
	<script type="text/javascript">
		/*遮罩层开始A*/
		function ajaxLoadBegin(){
			$("<div class=\"datagrid-mask\"></div>").css({display:"block",width:"100%",height:$(window).height()}).appendTo("body");
			$("<div class=\"datagrid-mask-msg\"  style=\"font-size:12px;\"></div>").html("正在处理，请稍候。。。").appendTo("body").css({display:"block",left:($(document.body).outerWidth(true) - 190) / 2,top:($(window).height() - 45) / 2});
		}
		/*遮罩层结束B*/
		function ajaxLoadEnd(){
			$(".datagrid-mask").remove();
			$(".datagrid-mask-msg").remove();
		}
		function loginFun() {
			if(!$("#loginForm").form('validate')){
				return ;
			}
			ajaxLoadBegin();
			var password = $('#TxtPassword').val();
			var userName = $('#TxtUserName').val();
			$.post('login/login_toLogin.action', {
				Password: $.md5(password),
				UserName: userName
			}, function (result) {
				if (result == 'true') {
					ajaxLoadEnd();
					window.location = "login/index_toDefault.action";
				} else {
					$.messager.alert('错误', "用户名或密码错误！", 'error');
				}
			}, 'json');
		}
	</script>
</html>