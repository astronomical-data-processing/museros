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
<script type="text/javascript" src="lib/jquery/jquery.easing.min.js"></script>
<style type="text/css">
    #content {
        width: 980px;
        margin: 10px auto;
    }

    .seperater {
        height: 25px;
    }

    .list-img {
        width: 100px;
        height: 120px;
        border: 1px solid #ccc;
        padding: 1px;
        box-shadow: 0 3px 3px rgba(0, 0, 0, 0.3);
        float: left;
    }

    .list-img-desc {
        margin-left: 10px;;
        border: 1px solid #ccc;
        padding: 10px;
        float: left;
        width: 842px;
        height: 100px;
        box-shadow: 0 2px 2px rgba(0, 0, 0, 0.3);
    }

    .list-clear {
        clear: left;
    }

    .list-tag {
        font-weight: bold;
        margin-right: 10px;
    }

    .list-wrapper {
        margin: 20px auto;
    }

    .content-wrapper {
        padding-top: 10px;;
    }

    .list-img-link {
        text-align: right;;
    }

    #main {
        min-height: 600px;
        maring: 30px 0 20px;
    }
</style>
<!-- main -->
<div class="main" id="main">
    <!-- shell -->
    <div class="shell">
        <div class="container"><h1>Processed Images List</h1>

            <div class="easyui-panel" style="margin-top:10px;">
                <div class="easyui-pagination" id="imagePage" data-options="
                         layout:['list','sep','first','prev','links','next','last','sep','refresh']"></div>
            </div>
            <!--list-wrapper-container begin-->
            <div id="list-wrapper-container">
                <div id="list-wrapper" class="list-wrapper">
                    Loading Image Items......
                </div>
            </div>
            <!--list-wrapper-container end-->
        </div>
        <script type="text/javascript">
            $(document).ready(function () {
                $("#imagePage").pagination({
                    pageSize: 10,
                    pageNumber: 1,
                    pageList: [10, 20, 30],
                    loading: false,
                    onSelectPage: function (pageNumber, pageSize) {
                        var me = this;
                        $.post('image_query.action', {
                            pageNumber: pageNumber,
                            pageSize: pageSize
                        }, function (result) {
                            $(me).pagination('loading');
                            $(me).pagination('refresh', {
                                total: result.total
                            });
                            $(me).pagination('loaded');
                            parseContent(result);
                        }, 'json');
                    }
                });
                $('#imagePage').pagination('select');
                $('#pp').pagination('refresh', {	// change options and refresh pager bar information
                    total: 114
                });
            });
            function formatDateTime(val) {
                var value;
                try {
                    value = new Date(val).toLocaleString();
                } catch (e) {
                    value = val;
                }
                return value;
            }
            function parseContent(result) {
                var record = result.rows;
                var len = result.rows.length;
                if (result && result.rows && len > 0) {
                    var html;
                    var imageList = "";
                    for (var i = 0; i < len; i++) {
                        html = "";

                        html = '<div id="list-wrapper-container">';
                        html += '    <div class="list-wrapper">';
                        html += '        <img class="list-img"  src="' + record[i].imagePath + '" alt="' + record[i].name + '">';
                        html += '        <div class="list-img-desc">';
                        html += '            <div class="list-img-title"><span class="list-tag">Title:</span><span>' + record[i].name + '</span></div>';
                        html += '            <div class="list-img-text"><span class="list-tag">Description:</span><span>' + record[i].description + '</span></div>';
                        html += '            <div class="list-img-date"><span class="list-tag">Date:</span>' + formatDateTime(record[i].createDate) + '</div>';
                        html += '            <div class="list-img-link"><a href=image_detail.action?token=XDSDEWRSXDFASDF&imageID=' + record[i].imageID + '>View Detail>></a></div>';
                        html += '        </div>';
                        html += '        <div class="list-clear"></div>';
                        html += '    </div>';
                        html += '</div>';

                        imageList += html;
                    }
                    $("#list-wrapper-container").hide({
                        duration: 500,
                        easing: 'linear',
                        complete: function () {
                            $("#list-wrapper-container div[class=list-wrapper]").remove();
                        }
                    });

                    $("#list-wrapper-container").show({
                        duration: 1000,
                        easing: 'linear',
                        complete: function () {
                            $("#list-wrapper-container").append(imageList);
                        }
                    });
                } else {
                    $.messager.alert('Error', "Server can not process request.", 'error');
                }
            }
        </script>
    </div>
</div>
</body>
</html>