package org.cnlab.admin.model;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * Created by cnlab on 2015/1/24.
 */
@Entity
@Table(name = "T_User")
public class UserModel {

    private int UserID;
    //用户名
    private String UserName;
    //密码
    private String Password;
    //状态
    private boolean Status;
    //建立日期
    private Timestamp CreateTime;
    //修改日期
    private Timestamp ModifiedTime;
    //姓名
    private String Name;
    //盐值
    private String Salt;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "UserID")
    public int getUserID() {
        return UserID;
    }

    public void setUserID(int userID) {
        UserID = userID;
    }

    @Column(name = "UserName", length = 20)
    public String getUserName() {
        return UserName;
    }

    public void setUserName(String userName) {
        UserName = userName;
    }

    @Column(name = "Password", length = 64, updatable = false)
    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }

    @Column(name = "Status", length = 1, updatable = false)
    public boolean isStatus() {
        return Status;
    }

    public void setStatus(boolean status) {
        Status = status;
    }

    @Column(name = "CreateTime", updatable = false)
    public Timestamp getCreateTime() {
        return CreateTime;
    }

    public void setCreateTime(Timestamp createTime) {
        CreateTime = createTime;
    }

    @Column(name = "ModifiedTime")
    public Timestamp getModifiedTime() {
        return ModifiedTime;
    }

    public void setModifiedTime(Timestamp modifiedTime) {
        ModifiedTime = modifiedTime;
    }

    @Column(name = "Salt", length = 36, updatable = false)
    public String getSalt() {
        return Salt;
    }

    public void setSalt(String salt) {
        Salt = salt;
    }

    //姓名
    @Column(name = "Name")
    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

}
