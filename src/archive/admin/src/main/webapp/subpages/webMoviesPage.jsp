<%--
  Created by IntelliJ IDEA.
  User: LiuYingBo
  Date: 2015/2/1
  Time: 11:08
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <jsp:include page="headerTemplate.jsp"></jsp:include>
    <style>
        p, h2, ul, li {
            margin: 0px;
            padding: 0px;
        }

        li {
            margin-left: 50px;
        }

        h2 {
            color: white;
        }

        #shortbar a {
            color: white;
            text-decoration: none;
            padding: 1px 5px 0px 5px;
        }

        #shortbar a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
<table id="dg" title="动画列表" class="easyui-datagrid"
       url="../login/user_query.action?"
       toolbar="#toolbar" pagination="true"
       rownumbers="true" fitColumns="true" singleSelect="true">
    <thead>
    <tr>
        <th field="name" width="20">动画名称</th>
        <th field="moviePath" width="20">动画所在路径</th>
        <th field="type" width="20">动画类型</th>
        <th field="description" width="10" hidden=true>描述</th>
        <th field="createDate" formatter=formatDateTime width="20">创建时间</th>
    </tr>
    </thead>
</table>
<div id="toolbar">
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-add" plain="true" onclick="newUser()">新增动画</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-edit" plain="true"
       onclick="editUser()">编辑动画</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-remove" plain="true" onclick="destroyUser()">删除动画</a>
</div>
<div id="dlg" class="easyui-dialog" style="width:450px;height:250px;top:30px;padding:10px 20px"
     closed="true" buttons="#dlg-buttons" data-options="iconCls:'icon-save',resizable:true,modal:true">
    <div class="ftitle">用户信息</div>
    <form id="fm" method="post" novalidate>
        <div class="fitem">
            <label>用户名:</label>
            <input name="name" class="easyui-textbox" required="true" validtype="CHS">
        </div>
        <div class="fitem">
            <label>登录账号:</label>
            <input name="userName" class="easyui-textbox" required="true" validtype="account[3,20]">
        </div>

    </form>
    <div>提示：登录账号用于登录系统</div>
</div>
<div id="dlg-buttons">
    <a href="javascript:void(0)" class="easyui-linkbutton c6" iconCls="icon-ok" onclick="saveUser()" style="width:90px">保存</a>
    <a href="javascript:void(0)" class="easyui-linkbutton" iconCls="icon-cancel"
       onclick="javascript:$('#dlg').dialog('close')" style="width:90px">取消</a>
</div>
<script type="text/javascript">
    window.parent.window.ajaxLoadEnd();
    function formatDateTime(val,row){
        var value;
        try {
            value = new Date(val).toLocaleString();
        } catch (e){
            value=val;
        }
        return value;
    };
    var url;
    function newUser() {
        $('#dlg').dialog('open').dialog('setTitle', '新增用户');
        $('#fm').form('clear');
        url = '../login/user_add.action';
    }
    function editUser() {
        var row = $('#dg').datagrid('getSelected');
        if (row) {
            $('#dlg').dialog('open').dialog('setTitle', '修改用户');
            $('#fm').form('load', row);
            url = '../login/user_edit.action?UserID=' + row.userID;
        }else{
            $.messager.alert("操作提示", "请选择需要修改的用户!","info");
        }
    }
    function saveUser() {
        $('#fm').form('submit', {
            url: url,
            onSubmit: function () {
                return $(this).form('validate');
            },
            success: function (result) {
                var result = eval('(' + result + ')');
                if (result.errorMsg) {
                    $.messager.show({
                        title: 'Error',
                        msg: result.errorMsg
                    });
                } else {
                    $('#dlg').dialog('close'); // close the dialog
                    $('#dg').datagrid('reload'); // reload the user data
                }
            }
        });
    }
    function destroyUser() {
        var row = $('#dg').datagrid('getSelected');
        if (row) {
            $.messager.confirm('提示', '确定要删除该用户?', function (r) {
                if (r) {
                    $.post('../login/user_delete.action', {UserID: row.userID}, function (result) {
                        if (result.success) {
                            $('#dg').datagrid('reload'); // reload the user data
                        } else {
                            $.messager.show({ // show error message
                                title: '错误',
                                msg: result.errorMsg
                            });
                        }
                    }, 'json');
                }
            });
        }
    }
</script>

<style type="text/css">
    #fm {
        margin: 0;
        padding: 10px 30px;
    }

    .ftitle {
        font-size: 14px;
        font-weight: bold;
        padding: 5px 0;
        margin-bottom: 10px;
        border-bottom: 1px solid #ccc;
    }

    .fitem {
        margin-bottom: 5px;
    }

    .fitem label {
        display: inline-block;
        width: 80px;
    }

    .fitem input {
        width: 160px;
    }
</style>
</body>
</html>
