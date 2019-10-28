package org.cnlab.admin.model;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * Created by cnlab on 2015/1/24.
 */
@Entity
@Table(name = "T_Search")
public class SearchModel {
    //搜索ID
    private int SearchID;
    //查找路径
    private String SearchPath;
    //状态
    private boolean Status;
    //建立日期
    private Timestamp CreateTime;
    //修改日期
    private Timestamp ModifiedTime;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "SearchID")
    public int getSearchID() {
        return SearchID;
    }

    public void setSearchID(int searchID) {
        SearchID = searchID;
    }

    @Column(name = "CreateTime")
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

    @Column(name = "SearchPath", length = 256)
    public String getSearchPath() {
        return SearchPath;
    }

    public void setSearchPath(String searchPath) {
        SearchPath = searchPath;
    }

    @Column(name = "Status", length = 1)
    public boolean isStatus() {
        return Status;
    }

    public void setStatus(boolean status) {
        Status = status;
    }

}
