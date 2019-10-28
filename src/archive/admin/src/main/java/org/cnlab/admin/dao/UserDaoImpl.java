package org.cnlab.admin.dao;

import org.cnlab.admin.model.UserModel;
import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("userDao")
public class UserDaoImpl extends BaseDaoImpl<UserModel> implements IUserDao {

}
