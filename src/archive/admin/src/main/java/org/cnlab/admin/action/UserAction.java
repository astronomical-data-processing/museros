package org.cnlab.admin.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.admin.model.UserModel;
import org.cnlab.admin.service.IUserService;
import org.cnlab.common.QueryModel;
import org.cnlab.common.utils.CommonHelper;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;


/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
@Controller
public class UserAction {
    @Resource(name = "userService")
    private IUserService userService;
    private int page;
    private int rows;

    private int UserID;
    private String UserName;
    private String Password;
    private String Name;
    private int currentPage;
    private int pageSize;

    private JSONObject result = new JSONObject();
    private String ajaxResult;

    public String add() throws Exception {
        String password = "888888";
        password = CommonHelper.getMD5(password);
        UserModel userModel = new UserModel();
        userModel.setName(getName());
        userModel.setUserName(getUserName());
        userModel.setPassword(password);
        String salt = CommonHelper.getUUID();
        userModel.setSalt(salt);
        userModel.setPassword(CommonHelper.calculatePassword(salt, password));

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        java.util.Date utilDate = new Date();
        java.sql.Timestamp sqlDate = new Timestamp(utilDate.getTime());

        userModel.setCreateTime(sqlDate);
        userModel.setModifiedTime(sqlDate);
        userService.save(userModel);
        return "SUCCESS";
    }

    public String edit() throws Exception {
        UserModel userModel = new UserModel();
        userModel.setUserID(getUserID());
        userModel.setUserName(getUserName());
        userModel.setName(getName());

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        java.util.Date utilDate = new Date();
        java.sql.Timestamp sqlDate = new Timestamp(utilDate.getTime());
        userModel.setModifiedTime(sqlDate);
        userService.update(userModel);
        return "SUCCESS";
    }

    public String delete() throws Exception {
        UserModel userModel = new UserModel();
        userModel.setUserID(getUserID());
        userService.delete(userModel);
        result.put("success",true);
        return "SUCCESS";
    }

    public String query() {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = page;
        queryModel.pageSize = rows;
        long totalCount = userService.queryAllUserCounts();
        List<UserModel> userModelList = userService.queryUsers(queryModel);
        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (userModelList != null) {
            results.put("rows", userModelList);
        }
        results.put("total", totalCount);
        String rows = JSON.toJSONString(results);
        result = (JSONObject) JSON.parse(rows);

        return "SUCCESS";
    }

    public JSONObject getResult() {
        return result;
    }

    public void setResult(JSONObject result) {
        this.result = result;
    }

    public String getAjaxResult() {
        return ajaxResult;
    }

    public void setAjaxResult(String ajaxResult) {
        this.ajaxResult = ajaxResult;
    }

    public String getUserName() {
        return UserName;
    }

    public void setUserName(String userName) {
        UserName = userName;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }


    public int getCurrentPage() {
        return currentPage;
    }

    public void setCurrentPage(int currentPage) {
        this.currentPage = currentPage;
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

    public int getUserID() {
        return UserID;
    }

    public void setUserID(int userID) {
        UserID = userID;
    }


    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getRows() {
        return rows;
    }

    public void setRows(int rows) {
        this.rows = rows;
    }

}
