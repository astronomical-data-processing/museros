package org.cnlab.admin.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.admin.model.UserModel;
import org.cnlab.admin.service.ILoginService;
import org.cnlab.common.utils.CommonHelper;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;


/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
@Controller
public class AdminAction {

    UserModel adminUser;
    @Resource(name = "loginService")
    private ILoginService loginService;
    private JSONObject result;
    private String ajaxResult;

    public UserModel getAdminUser() {
        return adminUser;
    }

    public void setAdminUser(UserModel adminUser) {
        this.adminUser = adminUser;
    }

    public String resetAdmin() {
        String adminName = "admin";
        String password = "888888";
        password = CommonHelper.getMD5(password);
        UserModel adminUser = new UserModel();
        adminUser.setUserName("admin");
        adminUser.setName("系统超级管理员");
        adminUser.setStatus(true);
        String salt = CommonHelper.getUUID();
        adminUser.setSalt(salt);
        adminUser.setPassword(CommonHelper.calculatePassword(salt, password));
        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        java.util.Date utilDate = new Date();
        java.sql.Timestamp sqlDate = new Timestamp(utilDate.getTime());
        adminUser.setCreateTime(sqlDate);
        adminUser.setModifiedTime(sqlDate);

        UserModel returnModel = loginService.checkUserNameIsValid(adminName);
        if (returnModel != null) {
            result = new JSONObject();
            try {
                adminUser.setUserID(returnModel.getUserID());
                loginService.updatePassword(adminUser);
                result.put("oper", "用户名已经存在，成功重置密码");
            } catch (Exception e) {
                result.put("oper", "用户名已经存在，重置密码异常");
            }
        } else {

            String rows = JSON.toJSONString(adminUser);
            result = (JSONObject) JSON.parse(rows);

            boolean returnResult = true;
            try {
                returnResult = loginService.resetAdmin(adminUser);
            } catch (Exception e) {
                returnResult = false;
            }
            if (returnResult) {
                ajaxResult = "管理员账号重置成功";
            } else {
                ajaxResult = "管理员账号重置失败";
            }
            result.put("oper", ajaxResult);
        }
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

}
