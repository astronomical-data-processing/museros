package org.cnlab.admin.dao;

import org.cnlab.admin.model.UserModel;
import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("loginDao")
public class LoginDaoImpl extends BaseDaoImpl<UserModel> implements ILoginDao {

}
