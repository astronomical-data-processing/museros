package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.dao.ILoginDao;
import org.cnlab.admin.model.UserModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * Created by cnlab on 2015/1/24.
 */
@Service("loginService")
public class LoginServiceImpl implements ILoginService {
    private static final Logger logger = Logger.getLogger(LoginServiceImpl.class);

    @Resource(name = "loginDao")
    private ILoginDao loginDao;

    @Override
    public UserModel isUserValid(String UserName, String Password) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("userName", UserName);
        map.put("password", Password);
        List<UserModel> userList = loginDao.find("from UserModel as u where u.userName=:userName and u.password=:password", map);
        if (userList.size() > 0) {
            return userList.get(0);
        } else {
            return null;
        }
    }

    @Override
    public UserModel findUserByName(String userName) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("userName", userName);
        List<UserModel> userList = loginDao.find("from UserModel as u where u.userName=:userName", map);
        if (userList.size() > 0) {
            return userList.get(0);
        } else {
            return null;
        }
    }

    @Override
    public boolean resetAdmin(UserModel adminUser) throws Exception {
        logger.info("At " + new java.util.Date().toLocaleString() + "resetAdmin");
        boolean flag = false;
        try {
            loginDao.save(adminUser);
            flag = true;
        } catch (Exception e) {
            logger.error("saveUserInfo error" + e.toString());
            throw e;
        }
        return flag;
    }

    @Override
    public UserModel checkUserNameIsValid(String adminName) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("userName", adminName);
        List<UserModel> userList = loginDao.find("from UserModel as u where u.userName=:userName", map);
        if (userList.size() > 0) {
            return userList.get(0);
        } else {
            return null;
        }
    }

    @Override
    public void updatePassword(UserModel adminUser) throws Exception {
        try {
            loginDao.update(adminUser);
        } catch (Exception e) {
            logger.error("updatePassword error" + e.toString());
            throw e;
        }
    }
}
