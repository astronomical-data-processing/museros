package org.cnlab.admin.service;

import org.cnlab.admin.model.UserModel;
import org.cnlab.common.QueryModel;

import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public interface IUserService {
    /**
     0* @param userModel
     * @return
     */
    void save(UserModel userModel) throws Exception;

    void update(UserModel userModel) throws Exception;

    void delete(UserModel userModel) throws Exception;

    List<UserModel> queryUsers(QueryModel queryModel);

    long queryAllUserCounts();
}
