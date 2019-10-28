package org.cnlab.admin.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.admin.model.MovieModel;
import org.cnlab.admin.service.IMovieService;
import org.cnlab.common.QueryModel;
import org.cnlab.common.utils.CommonHelper;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;


/**
 * @Project: mmovie
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
@Controller
public class MovieAction {
    @Resource(name = "movieService")
    private IMovieService movieService;
    private int page;
    private int rows;

    private int MovieID;
    private String MovieName;
    private String Password;
    private String Name;
    private int currentPage;
    private int pageSize;

    private JSONObject result = new JSONObject();
    private String ajaxResult;

    public String add() throws Exception {
        String password = "888888";
        password = CommonHelper.getMD5(password);
        MovieModel movieModel = new MovieModel();
        movieModel.setName(getName());
        String salt = CommonHelper.getUUID();

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());

        movieService.save(movieModel);
        return "SUCCESS";
    }

    public String edit() throws Exception {
        MovieModel movieModel = new MovieModel();
        movieModel.setMovieID(getMovieID());
        movieModel.setName(getName());

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());
        movieService.update(movieModel);
        return "SUCCESS";
    }

    public String delete() throws Exception {
        MovieModel movieModel = new MovieModel();
        movieModel.setMovieID(getMovieID());
        movieService.delete(movieModel);
        result.put("success",true);
        return "SUCCESS";
    }

    public String query() {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = page;
        queryModel.pageSize = rows;
        long totalCount = movieService.queryAllMovieCounts();
        List<MovieModel> movieModelList = movieService.queryMovies(queryModel);
        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (movieModelList != null) {
            results.put("rows", movieModelList);
        }
        results.put("total", totalCount);
        String rows = JSON.toJSONString(results);
        result = (JSONObject) JSON.parse(rows);

        return "SUCCESS";
    }

    public JSONObject getResult() {
        return result;
    }

    public void setResult(JSONObject result) {
        this.result = result;
    }

    public String getAjaxResult() {
        return ajaxResult;
    }

    public void setAjaxResult(String ajaxResult) {
        this.ajaxResult = ajaxResult;
    }

    public String getMovieName() {
        return MovieName;
    }

    public void setMovieName(String movieName) {
        MovieName = movieName;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }


    public int getCurrentPage() {
        return currentPage;
    }

    public void setCurrentPage(int currentPage) {
        this.currentPage = currentPage;
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

    public int getMovieID() {
        return MovieID;
    }

    public void setMovieID(int movieID) {
        MovieID = movieID;
    }


    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getRows() {
        return rows;
    }

    public void setRows(int rows) {
        this.rows = rows;
    }

}
