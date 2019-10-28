package org.cnlab.common;

import com.opensymphony.xwork2.ActionInvocation;
import com.opensymphony.xwork2.interceptor.AbstractInterceptor;
import org.apache.log4j.Logger;
import org.apache.struts2.StrutsStatics;

import javax.servlet.http.HttpServletRequest;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public class ErrorInterceptor extends AbstractInterceptor {

    @Override
    public String intercept(ActionInvocation actionInvocation) throws Exception {

        String result = null; // Action的返回值
        try {
            // 运行被拦截的Action,期间如果发生异常会被catch住
            result = actionInvocation.invoke();
            return result;
        } catch (Exception e) {
            /**
             * 处理异常
             */
            String errorMsg = "出现错误信息，请查看日志！";
            //通过instanceof判断到底是什么异常类型
            if (e instanceof RuntimeException) {
                //未知的运行时异常
                RuntimeException re = (RuntimeException) e;
                //re.printStackTrace();
                errorMsg = re.getMessage().trim();
            }
            //把自定义错误信息
            HttpServletRequest request = (HttpServletRequest) actionInvocation .getInvocationContext().get(StrutsStatics.HTTP_REQUEST);
            /**
             * 发送错误消息到页面
             */
            request.setAttribute("errorMsg", errorMsg);

            /**
             * log4j记录日志
             */
            Logger logger = Logger.getLogger(actionInvocation.getAction().getClass());
            logger.error(errorMsg, e);
            return "errorMsg";
        }//
    }
}

