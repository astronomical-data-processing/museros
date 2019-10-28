package org.cnlab.common;

import com.opensymphony.xwork2.ActionInvocation;
import com.opensymphony.xwork2.interceptor.AbstractInterceptor;
import org.apache.struts2.ServletActionContext;
import org.cnlab.admin.model.UserModel;

import javax.servlet.http.HttpServletResponse;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class SessionIterceptor extends AbstractInterceptor {

    @Override
    public String intercept(ActionInvocation ai) throws Exception {
//取得请求的URL
        String url = ServletActionContext.getRequest().getRequestURL().toString();
        HttpServletResponse response = ServletActionContext.getResponse();
        response.setHeader("Pragma", "No-cache");
        response.setHeader("Cache-Control", "no-cache");
        response.setHeader("Cache-Control", "no-store");
        response.setDateHeader("Expires", 0);
        UserModel systemUser = null;
        //对登录与注销请求直接放行,不予拦截
        if (url.indexOf("login_toLogin.action") != -1 || url.indexOf("logout") != -1 || url.indexOf("admin") != -1) {
            return ai.invoke();
        } else {
            //验证Session是否过期
            if (!ServletActionContext.getRequest().isRequestedSessionIdValid()) {
                //session过期,转向session过期提示页,最终跳转至登录页面
                return "tologin";
            } else {
                systemUser = (UserModel) ServletActionContext.getRequest().getSession().getAttribute("systemUser");
                //验证是否已经登录
                if (systemUser == null) {
                    //尚未登录,跳转至登录页面
                    return "login";
                } else {
                    return ai.invoke();

                }
            }
        }
    }
}