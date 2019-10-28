package org.cnlab.admin.action;

import com.alibaba.fastjson.JSONObject;
import com.opensymphony.xwork2.ActionContext;
import org.apache.struts2.ServletActionContext;
import org.cnlab.admin.model.EventModel;
import org.cnlab.admin.model.UserModel;
import org.cnlab.admin.service.ILoginService;
import org.cnlab.common.Constants;
import org.cnlab.common.NetworkHelper;
import org.cnlab.common.utils.CommonHelper;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by cnlab on 2015/1/24.
 */
@Controller
public class LoginAction {
    private JSONObject result;
    private String ajaxResult;
    private String UserName;
    private String Password;
    private String ValidCode;

    @Resource(name = "loginService")
    private ILoginService loginService;

    @Resource(name = "eventService")
    private org.cnlab.admin.service.IEventService eventService;

    public String toLogin() {
        UserModel user = loginService.findUserByName(UserName);
        if (user == null) {
            ajaxResult = "用户名或密码错误。";
            return "SUCCESS";
        }
        String salt = user.getSalt();
        String calPassword = CommonHelper.calculatePassword(salt, getPassword());

        HashMap<Object, Object> results = new HashMap<Object, Object>();
        UserModel users = loginService.isUserValid(UserName, calPassword);
        if (users != null) {
            ajaxResult = "true";
        } else {
            ajaxResult = "用户名或密码错误";
        }
        ActionContext.getContext().getSession().put(Constants.LOGONUSER,UserName);
        //记录日志
        EventModel event = new EventModel();
        event.setUserName(UserName);
        event.setEventName("用户登录");
        event.setOperation("用户尝试登录系统");

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        java.util.Date utilDate = new Date();
        java.sql.Timestamp sqlDate = new Timestamp(utilDate.getTime());
        event.setEventDateTime(sqlDate);

        event.setIP(NetworkHelper.getIpAddr(ServletActionContext.getRequest()));
        writeLog(event);
        return "SUCCESS";
    }

    public String toLogout() {
        //记录日志
        EventModel event = new EventModel();
        UserName = (String)ActionContext.getContext().getSession().get(Constants.LOGONUSER);
        event.setUserName(UserName);
        event.setEventName("用户退出");
        event.setOperation("在用户成功退出系统");

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());
        event.setEventDateTime(sqlDate);

        event.setIP(NetworkHelper.getIpAddr(ServletActionContext.getRequest()));
        writeLog(event);

        Map session = ActionContext.getContext().getSession();
        session.remove(Constants.LOGONUSER);
        session.clear();

        return "toLogin";
    }

    private void writeLog(EventModel event) {

        try {
            eventService.insertEvent(event);
        }catch(Exception e)
        {

        }
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

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }

    public String getUserName() {
        return UserName;
    }

    public void setUserName(String userName) {
        UserName = userName;
    }

    public String getValidCode() {
        return ValidCode;
    }

    public void setValidCode(String validCode) {
        ValidCode = validCode;
    }

}
