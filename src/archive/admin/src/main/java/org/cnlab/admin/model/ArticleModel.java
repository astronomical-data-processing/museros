package org.cnlab.admin.model;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * Created by cnlab on 2015/1/24.
 */
@Entity
@Table(name = "T_Article")
public class ArticleModel {
    //文章ID
    private int ArticleID;
    //标题
    private String Title;
    //内容
    private String Content;
    //状态
    private boolean Status;
    //建立日期
    private Timestamp CreateTime;
    //修改日期
    private Timestamp ModifiedTime;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ArticleID")
    public int getArticleID() {
        return ArticleID;
    }

    public void setArticleID(int articleID) {
        ArticleID = articleID;
    }

    @Column(name = "Content", length = 2000)
    public String getContent() {
        return Content;
    }

    public void setContent(String content) {
        Content = content;
    }

    @Column(name = "CreateTime", length = 20)
    public Timestamp getCreateTime() {
        return CreateTime;
    }

    public void setCreateTime(Timestamp createTime) {
        CreateTime = createTime;
    }

    @Column(name = "ModifiedTime", length = 20)
    public Timestamp getModifiedTime() {
        return ModifiedTime;
    }

    public void setModifiedTime(Timestamp modifiedTime) {
        ModifiedTime = modifiedTime;
    }

    @Column(name = "Status", length = 1)
    public boolean isStatus() {
        return Status;
    }

    public void setStatus(boolean status) {
        Status = status;
    }

    @Column(name = "Title", length = 100)
    public String getTitle() {
        return Title;
    }

    public void setTitle(String title) {
        Title = title;
    }


}
