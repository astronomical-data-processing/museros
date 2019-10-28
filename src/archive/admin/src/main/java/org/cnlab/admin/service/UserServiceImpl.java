package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.model.UserModel;
import org.cnlab.common.Constants;
import org.cnlab.common.QueryModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
@Service("userService")
public class UserServiceImpl implements IUserService {
    private static final Logger logger = Logger.getLogger(LoginServiceImpl.class);

    @Resource(name = "userDao")
    private org.cnlab.admin.dao.IUserDao userDao;
    /**
     * 0* @param userModel
     *
     * @param userModel
     * @return
     */
    @Override
    public void save(UserModel userModel) throws Exception {
        try {
            userDao.save(userModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void update(UserModel userModel) throws Exception {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("userName", userModel.getUserName());
        map.put("name", userModel.getName());
        map.put("modifiedTime", userModel.getModifiedTime());
        map.put("userID", userModel.getUserID());
        try {
            userDao.executeHQL("update UserModel u set u.userName=:userName,u.name=:name,u.modifiedTime=:modifiedTime where u.userID=:userID",map);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void delete(UserModel userModel) throws Exception {
        try {
            userDao.delete(userModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public List<UserModel> queryUsers(QueryModel queryModel) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("userName", Constants.SUPERADMIN);
        return userDao.find("from UserModel u where u.userName !=:userName",map,queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public long queryAllUserCounts() {
        return userDao.count(" select count(*) from UserModel");
    }
}
