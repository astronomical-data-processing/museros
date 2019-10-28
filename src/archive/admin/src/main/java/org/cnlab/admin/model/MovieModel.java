package org.cnlab.admin.model;

import javax.persistence.*;
import java.sql.Timestamp;

/**
 * Created by cnlab on 2015/1/24.
 */
@Entity
@Table(name = "T_Movie")
public class MovieModel {

    private int MovieID;
    //PNG,JPG...
    private String Type;
    //名称
    private String Name;
    //描述
    private String Description;
    //路径
    private String MoviePath;
    //时间
    private Timestamp CreateDate;
    //是否删除
    private boolean IsDeleted;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "MovieID")
    public int getMovieID() {
        return MovieID;
    }

    public void setMovieID(int MovieID) {
        MovieID = MovieID;
    }

    @Column(name = "IsDeleted", length = 1)
    public boolean isDeleted() {
        return IsDeleted;
    }

    public void setDeleted(boolean isDeleted) {
        IsDeleted = isDeleted;
    }

    @Column(name = "IsType", length = 2)
    public String getType() {
        return Type;
    }

    public void setType(String type) {
        Type = type;
    }

    @Column(name = "Name", length = 30)
    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

    @Column(name = "Description", length = 100)
    public String getDescription() {
        return Description;
    }

    public void setDescription(String description) {
        Description = description;
    }

    @Column(name = "MoviePath", length = 100)
    public String getMoviePath() {
        return MoviePath;
    }

    public void setMoviePath(String moviePath) {
        MoviePath = moviePath;
    }

    @Column(name = "CreateDate")
    public Timestamp getCreateDate() {
        return CreateDate;
    }

    public void setCreateDate(Timestamp createDate) {
        CreateDate = createDate;
    }


}
