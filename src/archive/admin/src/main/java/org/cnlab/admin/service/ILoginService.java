package org.cnlab.admin.service;


import org.cnlab.admin.model.UserModel;

/**
 * Created by cnlab on 2015/1/24.
 */
public interface ILoginService {
    public UserModel isUserValid(String UserName, String Password);

    UserModel findUserByName(String userName);

    boolean resetAdmin(UserModel adminUser) throws Exception;

    UserModel checkUserNameIsValid(String adminName);

    void updatePassword(UserModel adminUser) throws Exception;
}
